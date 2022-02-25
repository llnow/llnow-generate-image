def get_date(tweets_features):
    until = tweets_features['latest_tweet_created_at']
    year, month, day = map(int, until.split()[0].split('-'))

    return year, month, day
