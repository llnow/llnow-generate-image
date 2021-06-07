from posted_time_utc2jst import *
from parse2params import *


def fetch_tweets(twitter):
    # since_idを取得
    file = open('tmp/since_id.txt', 'r')
    since_id = file.read()
    file.close()

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
    for _ in range(max_api_request):
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
        print(next_results)
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
