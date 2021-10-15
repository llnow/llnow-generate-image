import boto3
import wordcloud
import random


def generate_wc(words, img_config, bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    # s3からフォントをダウンロード
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    bucket.download_file('fonts/ヒラギノ角ゴシック W6.ttc', font_path)

    # dynamodbからstopwordsを取得
    table = boto3.resource('dynamodb').Table('ll-now-wc-stopwords')
    res = table.scan()
    stopwords = [item['word'] for item in res['Items']]
    stopwords = set(stopwords)

    # dynamodbからcolormap_listを取得
    table = boto3.resource('dynamodb').Table('ll_now')
    primary_key = {'primary': 'colormap_list'}
    res = table.get_item(Key=primary_key)
    colormap_list = res['Item']['colormap']

    # colormapをランダムに決定
    colormap = random.choice(colormap_list)

    # wordcloudのサイズを指定
    width = img_config['img_width']
    height = img_config['wc_height']

    wc = wordcloud.WordCloud(
        font_path=font_path,
        width=width,
        height=height,
        # mask=msk,
        stopwords=stopwords,
        regexp=r"\w[\w']+|[\w]+[\w・]*[\w]+|[^ぁ-んァ-ン０-９0-9\-!#$%&'()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]",  # 漢字・アルファベット以外の一文字を除去
        background_color='white',
        colormap=colormap,
        include_numbers=False
    )
    wc.generate(words)

    wc.to_file('/tmp/wc.png')
