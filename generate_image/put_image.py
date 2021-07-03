import boto3


def put_image(bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    # image_path = '/tmp/post_image.png'
    # bucket.upload_file(image_path, 'tmp/post_image.png')
    image_path = '/tmp/wc.png'
    bucket.upload_file(image_path, 'tmp/wc.png')
