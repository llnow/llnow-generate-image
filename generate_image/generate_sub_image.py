import boto3
from PIL import Image, ImageDraw, ImageFont


def generate_sub_image(img_config):
    # サブイメージ作成に必要な情報をdynamodbから取得
    table = boto3.resource('dynamodb').Table('ll_now')
    primary_key = {'primary': 'tweets_feature'}
    res = table.get_item(Key=primary_key)
    tweets_feature = res['Item']['feature']
    n_tweet = tweets_feature['n_tweet']
    since = tweets_feature['oldest_tweet_created_at']
    until = tweets_feature['latest_tweet_created_at']

    # テキストを指定
    text_above_gen_from = 'Generated from '
    text_above_n_tweet = str(n_tweet)
    text_above_twt_w = ' Tweets with '
    text_above_hashtag = '#lovelive'
    text_above_in = ' in'
    text_below = '{}-{}'.format(since, until)
    text_right_above = '@LLNow_JP'
    text_right_below = '#LLNow'

    # 画像サイズ，マージンを取得
    img_width = img_config['img_width']
    img_height = img_config['sub_img_height']
    side_margin = img_config['sub_img_side_margin']
    tweet_range_left_margin = img_config['tweet_range_left_margin']

    # 背景画像を作成
    img = Image.new('RGB', (img_width, img_height), (220, 220, 220))
    # 描画インスタンスを宣言
    draw = ImageDraw.Draw(img)

    # フォントを指定
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    font_above = ImageFont.truetype(font_path, 60)
    font_below = ImageFont.truetype(font_path, 100)
    font_right = ImageFont.truetype(font_path, int((img_height - 10) / 2))

    # 描画
    width_above_gen_from = font_above.getsize(text_above_gen_from)[0]
    width_above_n_tweet = font_above.getsize(text_above_n_tweet)[0]
    width_above_twt_w = font_above.getsize(text_above_twt_w)[0]
    width_above_hashtag = font_above.getsize(text_above_hashtag)[0]
    draw.text((side_margin, 0),
              text_above_gen_from, font=font_above, fill='#333333')
    draw.text((side_margin + width_above_gen_from, 0),
              text_above_n_tweet, font=font_above, fill='#000')
    draw.text((side_margin + width_above_gen_from + width_above_n_tweet, 0),
              text_above_twt_w, font=font_above, fill='#333333')
    draw.text((side_margin + width_above_gen_from + width_above_n_tweet + width_above_twt_w, 0),
              text_above_hashtag, font=font_above, fill='#1DA1F2')
    draw.text((side_margin + width_above_gen_from + width_above_n_tweet + width_above_twt_w + width_above_hashtag, 0),
              text_above_in, font=font_above, fill='#333333')
    draw.text((side_margin + tweet_range_left_margin, 60), text_below, font=font_below, fill='#000')
    width_right_above = font_right.getsize(text_right_above)[0]
    width_right_below = font_right.getsize(text_right_below)[0]
    draw.text((img_width - max(width_right_above, width_right_below) - side_margin, 0),
              text_right_above, font=font_right, fill='#000')
    draw.text((img_width - max(width_right_above, width_right_below) - side_margin, (img_height - 10) / 2 + 5),
              text_right_below, font=font_right, fill='#1DA1F2')

    # 画像を保存
    img.save('/tmp/sub_image.png', quality=100, dpi=(600, 600), optimize=True)
