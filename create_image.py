import matplotlib.pyplot as plt
import wordcloud


def create_image(words):
    font_path = 'fonts/ヒラギノ角ゴシック W6.ttc'
    wc = wordcloud.WordCloud(font_path=font_path,
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
