import boto3
from PIL import Image, ImageDraw, ImageFont
from get_hashtags import *


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
    text_above_hashtag = ' '.join(get_hashtags())
    text_above_in = ' in'
    text_below = '{}-{} JST'.format(since, until)
    text_right_at = '@'
    text_right_username = 'LLNow_ jp'  # spaceを入れないと'_'と'j'が被る
    text_right_hash = '#'
    text_right_hashtag_body = 'LLNow'

    # 画像サイズ，マージン，フォントサイズ，背景色を取得
    img_width = img_config['img_width']
    img_height = img_config['sub_img_height']
    left_margin = img_config['sub_img_left_margin']
    right_margin = img_config['sub_img_right_margin']
    sub_img_above_font_size = img_config['sub_img_above_font_size']
    sub_img_below_font_size = img_config['sub_img_below_font_size']
    sub_img_right_font_size = int((img_height - 10) / 2)
    sub_img_bg_color = img_config['sub_img_bg_color']

    # 背景画像を作成
    img = Image.new('RGB', (img_width, img_height), sub_img_bg_color)
    # 描画インスタンスを宣言
    draw = ImageDraw.Draw(img)

    # フォントを指定
    font_path = '/tmp/ヒラギノ角ゴシック W6.ttc'
    font_above = ImageFont.truetype(font_path, sub_img_above_font_size)
    font_below = ImageFont.truetype(font_path, sub_img_below_font_size)
    font_right = ImageFont.truetype(font_path, sub_img_right_font_size)

    # フォントサイズを取得
    width_above_gen_from = font_above.getsize(text_above_gen_from)[0]
    width_above_n_tweet = font_above.getsize(text_above_n_tweet)[0]
    width_above_twt_w = font_above.getsize(text_above_twt_w)[0]
    width_above_hashtag = font_above.getsize(text_above_hashtag)[0]
    width_right_at = font_right.getsize(text_right_at)[0]
    width_right_username = font_right.getsize(text_right_username)[0]
    width_right_hash = font_right.getsize(text_right_hash)[0]
    width_right_hashtag_body = font_right.getsize(text_right_hashtag_body)[0]

    # 描画
    draw.text((left_margin, 0),
              text_above_gen_from, font=font_above, fill='#333333')
    draw.text((left_margin + width_above_gen_from, 0),
              text_above_n_tweet, font=font_above, fill='#000')
    draw.text((left_margin + width_above_gen_from + width_above_n_tweet, 0),
              text_above_twt_w, font=font_above, fill='#333333')
    draw.text((left_margin + width_above_gen_from + width_above_n_tweet + width_above_twt_w, 0),
              text_above_hashtag, font=font_above, fill='#1DA1F2')
    draw.text((left_margin + width_above_gen_from + width_above_n_tweet + width_above_twt_w + width_above_hashtag, 0),
              text_above_in, font=font_above, fill='#333333')
    draw.text((left_margin, sub_img_above_font_size), text_below, font=font_below, fill='#000')
    draw.text((img_width - max(width_right_username, width_right_hashtag_body) - width_right_at - right_margin, 0),
              text_right_at, font=font_right, fill='#000')
    draw.text((img_width - max(width_right_username, width_right_hashtag_body) - right_margin, 0),
              text_right_username, font=font_right, fill='#000')
    draw.text((img_width - max(width_right_username, width_right_hashtag_body) - width_right_hash - right_margin, sub_img_right_font_size + 5),
              text_right_hash, font=font_right, fill='#1DA1F2')
    draw.text((img_width - max(width_right_username, width_right_hashtag_body) - right_margin, sub_img_right_font_size + 5),
              text_right_hashtag_body, font=font_right, fill='#1DA1F2')

    # 画像を保存
    img.save('/tmp/sub_image.png', quality=100, dpi=(600, 600), optimize=True)
