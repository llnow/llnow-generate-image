import boto3
import matplotlib.pyplot as plt
import wordcloud
import random


def generate_wc(words, bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    # s3からフォントをダウンロード
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    bucket.download_file('fonts/ヒラギノ角ゴシック W6.ttc', font_path)

    colormap_list = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'spring', 'summer', 'autumn', 'winter', 'cool', 'ocean', 'gist_earth']
    wc = wordcloud.WordCloud(font_path=font_path,
                             background_color='white',
                             # mask=msk,
                             colormap=random.choice(colormap_list),
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
