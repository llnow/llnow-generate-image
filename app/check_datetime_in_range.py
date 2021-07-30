from datetime import datetime, timedelta, timezone


def check_datetime_in_range(since_str, until_str):
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)
    since = datetime.strptime(since_str+'+0900', '%Y-%m-%d %H:%M:%S%z')
    until = datetime.strptime(until_str+'+0900', '%Y-%m-%d %H:%M:%S%z')

    if since <= now <= until:
        return True
    else:
        return False
