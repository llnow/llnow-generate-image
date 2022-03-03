from get_mask_key import *

import boto3
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np

NAME_BUCKET_PROD = 'll-now-material'


def generate_masked_wc(words, mask_type, mask_requirements):
    s3 = boto3.resource('s3')
    bucket_prod = s3.Bucket(NAME_BUCKET_PROD)

    # s3からフォントをダウンロード
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    bucket_prod.download_file('fonts/ヒラギノ角ゴシック W6.ttc', font_path)

    # dynamodbからstopwordsを取得
    table = boto3.resource('dynamodb').Table('ll-now-wc-stopwords')
    res = table.scan()
    stopwords = [item['word'] for item in res['Items']]
    stopwords = set(stopwords)

    # maskのkeyを取得
    mask_key = get_mask_key(mask_type, mask_requirements)

    # maskを取得
    mask_path = '/tmp/mask.png'
    bucket_prod.download_file(mask_key, mask_path)
    mask_array = np.array(Image.open(mask_path))
    image_color = ImageColorGenerator(mask_array)

    wc = WordCloud(
        font_path=font_path,
        mask=mask_array,
        color_func=image_color,
        stopwords=stopwords,
        regexp="[\wΑ-ω]+[-\wΑ-ω・’.]*[\wΑ-ω]+|[\wΑ-ω]+",
        background_color='white',
        include_numbers=True,
        prefer_horizontal=1
    )
    wc.generate(words)

    wc.to_file('/tmp/wc.png')
