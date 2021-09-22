import boto3
from boto3.dynamodb.conditions import Attr
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image


def generate_wc(words, img_config, bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    # s3からフォントをダウンロード
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    bucket.download_file('fonts/ヒラギノ角ゴシック W6.ttc', font_path)

    # s3からマスク画像をダウンロード
    mask_img_path = '/tmp/mask.png'
    bucket.download_file('mask.png', mask_img_path)

    # dynamodbからstopwordsを取得
    table = boto3.resource('dynamodb').Table('ll-now-wc-stopwords')
    option = {
        'FilterExpression': Attr('category').ne('lovelive_basic')
    }
    res = table.scan(**option)
    stopwords = set([item['word'] for item in res['Items']])

    # wordcloudのサイズを指定
    width = img_config['img_width']
    height = img_config['wc_height']

    mask_array = np.array(Image.open(mask_img_path))
    image_color = ImageColorGenerator(mask_array)

    wc = WordCloud(
        font_path=font_path,
        width=width,
        height=height,
        mask=mask_array,
        color_func=image_color,
        stopwords=stopwords,
        background_color='white',
        collocations=False
    )
    wc.generate(words)

    wc.to_file('/tmp/wc.png')
