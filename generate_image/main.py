from fetch_words import *
from generate_post_image import *
from put_image import *


def main(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    words = fetch_words(bucket, key)
    generate_post_image(words, bucket)
    put_image(bucket)
