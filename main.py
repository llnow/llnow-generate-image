from fetch_tweets import *
from extract_texts import *
from extract_trend_words import *
from create_image import *
from post_tweet import *
from config import *
from requests_oauthlib import OAuth1Session

twitter = OAuth1Session(consumer_key, consumer_secret, token, token_secret)


def main():
    tweets, latest_tweet_posted_time, oldest_tweet_posted_time = fetch_tweets(twitter)
    texts = extract_texts(tweets)
    words = extract_trend_words(texts)
    create_image(words)
    post_tweet(latest_tweet_posted_time, oldest_tweet_posted_time, twitter)


if __name__ == '__main__':
    main()
