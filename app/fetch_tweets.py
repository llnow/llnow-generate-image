from posted_time_utc2jst import *
from parse2params import *
import boto3

BUCKET_NAME = 'll-now'

def fetch_tweets(twitter):
    # s3からsince_id.txtをダウンロード
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    text_path = '/tmp/since_id.txt'
    bucket.download_file('tmp/since_id.txt', text_path)

    # since_idを取得
    with open(text_path, 'r') as f:
        since_id = f.read()

    url_search = 'https://api.twitter.com/1.1/search/tweets.json'
    url_limit = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
    params = {
        'q': '#lovelive -filter:retweets',
        'lang': 'ja',
        'result_type': 'recent',
        'count': 100,
        'since_id': since_id
    }
    res = twitter.get(url_limit)
    contents = res.json()
    max_api_request = contents['resources']['search']['/search/tweets']['remaining']
    print('max_api_request: ' + str(max_api_request))
    tweets = []
    for req in range(max_api_request):
        if req != 0 and req % 10 == 0:
            print('{} requested'.format(req))
        res = twitter.get(url_search, params=params)
        contents = res.json()
        fetched_tweets = contents['statuses']
        if len(fetched_tweets) == 0:
            break
        for tweet in fetched_tweets:
            tweets.append(tweet)
        search_metadata = contents['search_metadata']
        next_results = search_metadata['next_results']
        since_id = search_metadata['since_id']
        next_results = next_results.lstrip('?')  # 先頭の?を削除
        params = parse2params(next_results)
        # 崩れるので上書き
        params['q'] = '#lovelive -filter:retweets'
        params['since_id'] = since_id

    latest_tweet = tweets[0]
    oldest_tweet = tweets[-1]
    latest_tweet_created_at = posted_time_utc2jst(latest_tweet['created_at'])
    oldest_tweet_created_at = posted_time_utc2jst(oldest_tweet['created_at'])
    n_fetched_tweets = len(tweets)
    # since_idを更新
    file = open('tmp/since_id.txt', 'w')
    updated_since_id = latest_tweet['id_str']
    file.write(updated_since_id)
    file.close()

    # res = twitter.get(url_search, params=params)
    # contents = res.json()
    # tweets = contents['statuses']
    #
    # latest_tweet = contents['statuses'][0]
    # oldest_tweet = contents['statuses'][-1]
    # latest_tweet_created_at = posted_time_utc2jst(latest_tweet['created_at'])
    # oldest_tweet_created_at = posted_time_utc2jst(oldest_tweet['created_at'])

    return tweets, n_fetched_tweets, latest_tweet_created_at, oldest_tweet_created_at
