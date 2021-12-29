from django.shortcuts import render
from django import forms
from django.http import HttpResponse
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.utils import to_categorical
import official.nlp.bert.bert_models
import official.nlp.bert.configs
import official.nlp.bert.run_classifier
import official.nlp.bert.tokenization as tokenization
from official.modeling import tf_utils
from official import nlp
from official.nlp import bert
import numpy as np
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import numpy
import pandas as pd
import tweepy, json
from selenium import webdriver
import contextlib
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import requests
import json
import tensorflow_text
import os
from google.cloud import storage
from django.conf import settings
import tempfile
import tempdir

# python manage.py runserver
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANFSXAEAAAAAjO7cmKc36feIo1rZ8WvVyDPejCk%3DZP7zBYzb3EYdYhbTUXRr1GGDJa4C0Cdu0XVQlOt1RKsUcMc75C"
ACCESS_TOKEN = "1230287486804537346-HvtK3mmgBBosjSFQoCxhdxlVp9rDmr"
ACCESS_SECRET_TOKEN = "A9mRqNBKIfqM4ysj6tHOzK6yenaG0gfDJnFShTl6ctiAx"
CONSUMER_KEY = "9FVlwpkqjETAWufOv9SEmHsUv"
CONSUMER_SECRET = "YbwfRMu9f2JzDdfxM1SQUrqxvAwjzbyNsXuPE5yhFvXf0fbjGo"


def home(request):

    return render(request, 'index.html')


def get_tweets(request):

    text_box_value = request.POST.get('text_box')
    if text_box_value:
        print("This is the value in the text box: ", text_box_value)
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)


        api = tweepy.API(auth)
        l = []
        query= text_box_value +" -is:retweet lang:en &max_results=10"# the - is a negation, we don't want re-tweets. For now we get english tweets
        tweets = searchTwitter(query,"tweet.fields=text" ,BEARER_TOKEN)


        data_for_df = json.load(open('data.json'))

        df_test = pd.DataFrame(data_for_df["data"])


        df_tweets = make_df(tweets)
        df_tweets = df_tweets.drop("id",axis=1)
        #df_tweets.to_csv('df_tweets.csv')
        tweets = df_tweets["text"].tolist()
        tweets = '\n\n\n\n\n\n\n\n\n'.join(str(x) for x in tweets)

        resp = requests.post("http://localhost:5000/", files={'file': open('data.json')}) # we can also make another request to another API that handles the helpfulness predictions
        print(resp.json())
        final_response = resp.json()
        preds = final_response['predictions']
        preds = '\n\n\n\n\n\n\n\n\n'.join(('Ratings Prediction: ')+str(x) for x in preds)

        return render(request, "index.html", {'output': preds,'tweets': tweets})


    else:
        return render(request, "index.html")



def searchTwitter(query,tweet_fields, bearer_token=BEARER_TOKEN):

    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields

    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def make_df(response):
    return pd.DataFrame(response['data'])






