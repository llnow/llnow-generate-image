import boto3
from boto3.dynamodb.conditions import Key
from check_datetime_in_range import *


def get_hashtags():
    table = boto3.resource('dynamodb').Table('ll-now-search-keyword')

    # 検索キーワードを取得
    # default_keywordsを取得
    res = table.query(
        KeyConditionExpression=Key('type').eq('default')
    )
    default_keywords = [d['keyword'] for d in res['Items']]

    # option_keywordsを取得
    res = table.query(
        KeyConditionExpression=Key('type').eq('option')
    )
    option_keywords = []
    option_list = res['Items']
    for option in option_list:
        kw = option['keyword']
        since_str = option['since']
        until_str = option['until']
        if check_datetime_in_range(since_str, until_str):
            option_keywords.append(kw)

    keywords = default_keywords + option_keywords

    return keywords
