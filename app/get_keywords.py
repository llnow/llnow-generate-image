def get_keywords(tweets_features):
    query = tweets_features['search_metadata']['query']
    keywords = query.split(' -filter')[0].split(' OR ')

    return keywords
