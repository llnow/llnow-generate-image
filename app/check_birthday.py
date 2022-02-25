from get_date import *
from boto3.dynamodb.conditions import Attr


def check_birthday(tweets_features):
    # ツイート収集期間の最終日の日付を取得
    year, month, day = get_date(tweets_features)

    table = boto3.resource('dynamodb').Table('lovelive-character')
    res = table.scan(
        FilterExpression=Attr('birthmonth').eq(month) & Attr('birthday').eq(day)
    )
    if res['Items']:
        flag_birthday = True
        birthday_character = res['Items'][0]
    else:
        flag_birthday = False
        birthday_character = None

    return flag_birthday, birthday_character
