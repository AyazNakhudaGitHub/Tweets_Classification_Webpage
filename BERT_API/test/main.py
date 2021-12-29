import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import official.nlp.bert.bert_models
import official.nlp.bert.configs
import official.nlp.bert.run_classifier
import official.nlp.bert.tokenization as tokenization
from official.modeling import tf_utils
from official import nlp
from official.nlp import bert
import numpy as np
import pandas as pd
import json
from flask import Flask, request, jsonify
import os


def get_ratings(x,tokenizer, max_seq_length, model):
    X_test = bert_encode(x, tokenizer, max_seq_length)
    y_pred = model.predict(X_test, batch_size=8, verbose=1)
    y_pred_bool = np.argmax(y_pred, axis=1) + 1
    return y_pred_bool



def encode_names(n, tokenizer):
   tokens = list(tokenizer.tokenize(n))
   tokens.append('[SEP]')
   return tokenizer.convert_tokens_to_ids(tokens)


def bert_encode(string_list, tokenizer, max_seq_length):
    num_examples = len(string_list)

    string_tokens = tf.ragged.constant([
        encode_names(n, tokenizer) for n in np.array(string_list)])

    cls = [tokenizer.convert_tokens_to_ids(['[CLS]'])] * string_tokens.shape[0]
    input_word_ids = tf.concat([cls, string_tokens], axis=-1)

    input_mask = tf.ones_like(input_word_ids).to_tensor(shape=(None, max_seq_length))

    type_cls = tf.zeros_like(cls)
    type_tokens = tf.ones_like(string_tokens)
    input_type_ids = tf.concat(
        [type_cls, type_tokens], axis=-1).to_tensor(shape=(None, max_seq_length))

    inputs = {
        'input_word_ids': input_word_ids.to_tensor(shape=(None, max_seq_length)),
        'input_mask': input_mask,
        'input_type_ids': input_type_ids}

    return inputs


app = Flask(__name__)

@app.route("/", methods =["GET", "POST"])
def index():
    if request.method == "POST":

        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:


            tweets = file.read()
            data_for_df = json.loads(tweets)
            df_tweets = pd.DataFrame(data_for_df["data"])

            max_seq_length = 512
            ratings_model = tf.keras.models.load_model('test/ml_models/Ratings_BERT_7')
            helpfulness_model = tf.keras.models.load_model('test/ml_models/helpfulness_model')
            bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2",trainable=True)
            vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
            do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
            tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)
            tokenizer.convert_tokens_to_ids(['[CLS]', '[SEP]'])

            #df_tweets.to_csv('df_tweets.csv')
            x = df_tweets.text.values
            predictions = get_ratings(x, tokenizer, 512, ratings_model)
            predictions = predictions.tolist()

            #helpfulness_predictions = get_ratings(x, tokenizer, 512, helpfulness_model) # you can also use the helpfulness model to see which comments are useful as a customer review
            #helpfulness_predictions = helpfulness_predictions.tolist()

            print(predictions)
            #print(helpfulness_predictions)
            #data = {"predictions": predictions, "helpfulness_predictions": helpfulness_predictions}
            data = {"predictions": predictions}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)

