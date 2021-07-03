def fetch_words(bucket, key):
    # 単語リストをs3からダウンロード
    file_path = '/tmp/' + key.split('/')[1]
    bucket.download_file(key, file_path)
    # ファイルを結合する
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = ' '.join(lines)

    return words
