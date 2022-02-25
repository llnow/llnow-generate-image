import boto3
import datetime


def check_special_mask(tweets_features):
    search_since = tweets_features['oldest_tweet_created_at']
    search_until = tweets_features['latest_tweet_created_at']

    # special_maskの時間を取得
    table = boto3.resource('dynamodb').Table('special-mask-timetable')
    res = table.scan()

    flag_special_mask = False
    img_basename = None
    for item in res['Items']:
        special_mask_since = item['since']
        special_mask_until = item['until']
        if check_if_2_time_range_overlap_each_other(search_since, search_until, special_mask_since, special_mask_until):
            flag_special_mask = True
            img_basename = item['img_basename']
            break

    return flag_special_mask, img_basename


def check_if_2_time_range_overlap_each_other(since1_str, until1_str, since2_str, until2_str):
    since1 = datetime.strptime(since1_str + '+0900', '%Y-%m-%d %H:%M:%S%z')
    until1 = datetime.strptime(until1_str + '+0900', '%Y-%m-%d %H:%M:%S%z')
    since2 = datetime.strptime(since2_str + '+0900', '%Y-%m-%d %H:%M:%S%z')
    until2 = datetime.strptime(until2_str + '+0900', '%Y-%m-%d %H:%M:%S%z')

    return not(until1 < since2 or until2 < since1)
