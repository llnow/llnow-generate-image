import boto3
import json


def read_tweets_features(bucket):
    key = 'tmp/tweets_features.json'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(key)
    response = obj.get()
    body = response['Body'].read()
    tweets_features = json.loads(body.decode('utf-8'))

    return tweets_features
