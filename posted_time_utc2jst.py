import datetime as dt
import time
import pytz


def posted_time_utc2jst(posted_time_utc):
    # time.struct_timeに変換
    st = time.strptime(posted_time_utc, '%a %b %d %H:%M:%S +0000 %Y')
    # datetimeに変換(timezoneを付与)
    utc_time = dt.datetime(st.tm_year, st.tm_mon, st.tm_mday,
                           st.tm_hour, st.tm_min, st.tm_sec, tzinfo=dt.timezone.utc)
    # 日本時間に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # フォーマットを変換
    jst_time_str = jst_time.strftime("%Y-%m-%d_%H%M%S")

    return jst_time_str
