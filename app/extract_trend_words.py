from janome.tokenizer import Tokenizer


def extract_trend_words(texts):
    t = Tokenizer()
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞']:
                words.append(token.base_form)

    return words
