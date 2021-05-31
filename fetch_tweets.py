from posted_time_utc2jst import *


def fetch_tweets(twitter):
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {
        'q': '#lovelive -filter:retweets',
        'lang': 'ja',
        'result_type': 'recent',
        'count': '3000'
    }
    res = twitter.get(url, params=params)
    contents = res.json()
    tweets = contents['statuses']

    latest_tweet = contents['statuses'][0]
    oldest_tweet = contents['statuses'][-1]
    latest_tweet_created_at = posted_time_utc2jst(latest_tweet['created_at'])
    oldest_tweet_created_at = posted_time_utc2jst(oldest_tweet['created_at'])

    return tweets, latest_tweet_created_at, oldest_tweet_created_at
