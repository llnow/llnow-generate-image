import boto3


def fetch_words(bucket, key):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    # 単語リストをs3からダウンロード
    file_path = '/tmp/' + key.split('/')[1]
    bucket.download_file(key, file_path)
    # ファイルを結合する
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = ' '.join(lines)

    return words
