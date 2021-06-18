from fetch_tweets import *
from extract_texts import *
from extract_trend_words import *
from create_image import *
from post_tweet import *
from requests_oauthlib import OAuth1Session
import os


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main(event, context):
    tweets, n_fetched_tweets, latest_tweet_posted_time, oldest_tweet_posted_time = fetch_tweets(twitter)
    texts = extract_texts(tweets)
    words = extract_trend_words(texts)
    create_image(words)
    post_tweet(n_fetched_tweets, latest_tweet_posted_time, oldest_tweet_posted_time, twitter)

