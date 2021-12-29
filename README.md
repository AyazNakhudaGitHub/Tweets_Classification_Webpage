# Tweets_Classification_Webpage




![Tweets_gif_2](https://user-images.githubusercontent.com/63979892/147628203-5e20c9a9-8f8d-4aaa-8615-44fab5040f55.gif)



The goal of this project is to be able to predict what rating a customer would give to a product. This enables businesses to better understand what customers think of their products as social media platforms such a Twitter and Youtube do not have rating systems.

This web application can search through Twitter and extract tweets which relate to a given keyword and classify the tweets into 5 categories. These categories represent ratings (out of 5) where 1 is bad and 5 is excellent. Ideally, the keywords should be products but, the webpage can also take in just about anything so long as people are talking about it on Twitter.  

This web application utilizes a neural network and BERT (Bidirectional Encoder Representations for Transformers) to make the classifications of the tweets. The machine learning models are based on the Is Bigger Better? Text Classification using state-of-the-art BERT with limited Compute research paper by: Ayaz Nakhuda, David Ferris and Jastejpal Soora. This paper can be visted using this link: https://github.com/AyazNakhudaGitHub/BERT_Customer_Reviews_Classification/blob/main/Report_Group_24.pdf

The programming language and modules used for this project inlcude: Python, Django, Flask, HTML5 and CSS3.

To run this project locally one will need to:

- Download all the files and maintain the directory structure.

- Ensure that you have all the neccessary modules installed.

- Download the machine learning models from the given drive link: https://drive.google.com/drive/folders/1S1WCRVz2fr8oZd7EysAFK36Lhwab0Eb6?usp=sharing

- Place the machine learning models into this directory: 'give the directory route here'

- Get the credentials for access to the Twitter API and input them into the file 'give the directory path here' and show the image of where to put the passwords

- Run the API 

- Type this command to get the wepage running

Future plans to host this web application and the API on the Google Cloud Platform is currently in the works. 



















While a GIF is included, a video is provided to give a live demo:

https://user-images.githubusercontent.com/63979892/147625800-65953f67-56ff-4e19-ab53-9239f3a48514.mp4

