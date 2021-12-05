import boto3
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np


def generate_masked_wc(words, bucket, birthday_character):
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

    # maskを取得
    series = birthday_character['series']
    first_name_en = birthday_character['first_name_en']
    mask_key = '/mask/LL-icon-mask/{}_icon/{}.png'.format(series, first_name_en)
    mask_path = '/tmp/mask.png'
    bucket.download_file(mask_key, mask_path)
    mask_array = np.array(Image.open(mask_path))
    image_color = ImageColorGenerator(mask_array)

    wc = WordCloud(
        font_path=font_path,
        mask=mask_array,
        color_func=image_color,
        stopwords=stopwords,
        regexp="[\wΑ-ω][\wΑ-ω]+|[\wΑ-ω]+[\wΑ-ω・’.]*[\wΑ-ω]+|[亜-腕纊-黑一-鿕a-zA-Z]",
        background_color='white',
        include_numbers=False
    )
    wc.generate(words)

    wc.to_file('/tmp/wc.png')
