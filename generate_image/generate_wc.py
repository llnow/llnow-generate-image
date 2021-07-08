import boto3
import wordcloud
import random


def generate_wc(words, img_config, bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    # s3からフォントをダウンロード
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    bucket.download_file('fonts/ヒラギノ角ゴシック W6.ttc', font_path)

    # wordcloudのサイズを指定
    width = img_config['img_width']
    height = img_config['wc_height']

    colormap_list = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'spring', 'summer', 'autumn', 'winter', 'cool', 'ocean', 'gist_earth']
    wc = wordcloud.WordCloud(font_path=font_path,
                             background_color='white',
                             # mask=msk,
                             colormap=random.choice(colormap_list),
                             stopwords={"もの", "これ", "ため", "それ", "ところ", "よう", "こと",
                                        "そう", "ます", "ので", "から", "など", "です", "する", "いる", "ない",
                                        "あり", "なく", "また", "その", "ある", "なっ", "てる", "この", "なり", "あれ",
                                        'ちゃん', '位', '日', '発売', '私', 'ん', 'さん', 'RT', '好き', 'の', '定期', 'フォロー'},
                             width=width, height=height)
    wc.generate(' '.join(words))

    wc.to_file('/tmp/wc.png')
