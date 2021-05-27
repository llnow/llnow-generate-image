from config import *
import json
from requests_oauthlib import OAuth1Session
import re
import matplotlib.pyplot as plt
from janome.tokenizer import Tokenizer
import wordcloud
import datetime as dt
import time
import pytz

twitter = OAuth1Session(consumer_key, consumer_secret, token, token_secret)


def main():
    tweets, latest_tweet_posted_time, oldest_tweet_posted_time = get_tweets()
    texts = get_texts(tweets)
    words = get_trend_words(texts)
    create_image(words)
    post_tweet(latest_tweet_posted_time, oldest_tweet_posted_time)


def get_tweets():
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


def posted_time_utc2jst(posted_time_utc):
    # time.struct_timeに変換
    st = time.strptime(posted_time_utc, '%a %b %d %H:%M:%S +0000 %Y')
    # datetimeに変換(timezoneを付与)
    utc_time = dt.datetime(st.tm_year, st.tm_mon, st.tm_mday,
                           st.tm_hour, st.tm_min, st.tm_sec, tzinfo=dt.timezone.utc)
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))  # 日本時間に変換
    jst_time_str = jst_time.strftime("%Y-%m-%d_%H%M%S")

    return jst_time_str


def get_texts(tweets):
    texts = []
    remove_words = ['lovelive', 'LoveLive', 'ラブライブ', 'Aqours', 'aqours', 'サンシャイン', '沼津', 'sunshine', '虹ヶ咲',
                    '虹ヶ咲学園スクールアイドル同好会', '同好会', 'Liella', 'スーパースター', 'ラブライバー', 'スクールアイドル', 'LoveLivestaff', 'スクフェス',
                    'スクスタ']
    for status in tweets:
        text = status['text']
        if text.startswith('RT '):
            continue
        # URLの除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', text)
        # 改行の除去
        # text=re.sub('\n', ' ', text)
        # 絵文字などの除去
        text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', '', text)
        for rm_word in remove_words:
            text = re.sub(rm_word, ' ', text)
        # print(text)
        # print('----------')
        texts.append(text)

    return texts


def get_trend_words(texts):
    t = Tokenizer()
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞']:
                words.append(token.base_form)

    return words


def create_image(words):
    wc = wordcloud.WordCloud(font_path='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
                             background_color='white',
                             # mask=msk,
                             # colormap = 'gray',
                             stopwords={"もの", "これ", "ため", "それ", "ところ", "よう", "こと",
                                        "そう", "ます", "ので", "から", "など", "です", "する", "いる", "ない",
                                        "あり", "なく", "また", "その", "ある", "なっ", "てる", "この", "なり", "あれ",
                                        'ちゃん', '位', '日', '発売', '私', 'ん', 'さん', 'RT', '好き', 'の', '定期', 'フォロー'},
                             width=800, height=600)
    wc.generate(' '.join(words))

    plt.figure(figsize=(15, 12))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

    # now = dt.datetime.now()
    #
    # time = now.strftime('%Y%m%d-%H%M%S')

    # wc.to_file('tmp/wc_{}.png'.format(time))
    wc.to_file('tmp/wc.png')


def post_tweet(latest_tweet_posted_time, oldest_tweet_posted_time):
    url_media = 'https://upload.twitter.com/1.1/media/upload.json'
    url_post = 'https://api.twitter.com/1.1/statuses/update.json'

    # 画像をアップロード
    files = {'media': open('tmp/wc.png', 'rb')}
    res_media = twitter.post(url_media, files=files)

    # レスポンスを確認
    if res_media.status_code != 200:
        print('Failed to upload media: {}'.format(res_media.text))
        exit()

    # media_id を取得
    media_id = json.loads(res_media.text)['media_id']

    # アップロードした画像を添付したツイートを投稿
    message = 'test\n' \
              + 'ツイート収集範囲：\n{}~{}\n'.format(oldest_tweet_posted_time, latest_tweet_posted_time) \
              + '#lovelive #LoveLiveNow'
    params = {'status': message, 'media_ids': [media_id]}
    res_post = twitter.post(url_post, params=params)

    # レスポンスを確認
    if res_post.status_code == 200:
        print("Success.")
    else:
        print("Failed.")
        print(" - Responce Status Code : {}".format(res_post.status_code))
        print(" - Error Code : {}".format(res_post.json()["errors"][0]["code"]))
        print(" - Error Message : {}".format(res_post.json()["errors"][0]["message"]))
        # {'errors': [{'code': 170, 'message': 'Missing required parameter: status.'}]}


if __name__ == '__main__':
    main()
