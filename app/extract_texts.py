import re


def extract_texts(tweets):
    texts = []
    remove_words = ['lovelive', 'LoveLive', 'ラブライブ', 'Aqours', 'aqours', 'サンシャイン', '沼津', 'sunshine', '虹ヶ咲',
                    '虹ヶ咲学園スクールアイドル同好会', '同好会', 'Liella', 'スーパースター', 'ラブライバー', 'スクールアイドル', 'LoveLivestaff', 'スクフェス',
                    'スクスタ']
    for status in tweets:
        text = status['text']
        if text.startswith('RT '):
            continue
        # URLの除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', text)
        # 改行の除去
        # text=re.sub('\n', ' ', text)
        # 絵文字などの除去
        text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', '', text)
        for rm_word in remove_words:
            text = re.sub(rm_word, ' ', text)
        # print(text)
        # print('----------')
        texts.append(text)

    return texts
