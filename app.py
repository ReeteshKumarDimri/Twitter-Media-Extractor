from flask import Flask, render_template, request, redirect, url_for
from config import *
import tweepy
import wget

#instantiating the api
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
#creating api object
api = tweepy.API(auth,wait_on_rate_limit=True)


def extract_media(media_files,key):
    for tweet in tweepy.Cursor(api.search_tweets, q=key).items(300):
       if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                img_src=image['media_url']
                media_files.add(img_src)


#Creating flask object
app=Flask(__name__)

#First Page.
@app.route("/")
def home_page():
    return render_template("form.html")

@app.route("/Fetch_Data",methods=['POST','GET'])

def Fetch_Data():
    if request.method=="POST":
        #retrieving keyword from the form.
        key=request.form["q"]
        #IF user do not enter anything then flash a warning.
        if key == "":
            return render_template("form.html",warning="Please enter a keyword !")
        #Otherwise, creating a empty set for media urls.
        media_sources=set()
        #extracting urls from media based on the keyword and saving them in the empty set.
        extract_media(media_sources,key)
        return render_template("form.html",media=media_sources)



if __name__ =="__main__":
    app.run(debug= True)

            