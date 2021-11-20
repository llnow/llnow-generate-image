from fetch_words import *
from config_img import *
from generate_post_image import *
from put_image import *


def main(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    mode = context.invoked_function_arn.split(':')[-1]

    words = fetch_words(bucket, key)
    img_config = config_img()
    generate_post_image(words, img_config, bucket, mode)
    put_image(bucket)
