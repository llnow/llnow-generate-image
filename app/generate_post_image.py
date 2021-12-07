from read_tweets_features import *
from check_birthday import *
from generate_masked_wc import *
from generate_wc import *
from generate_sub_image import *
from merge_image import *


def generate_post_image(words, img_config, bucket):
    tweets_features = read_tweets_features(bucket)
    flag_birthday, birthday_character = check_birthday(tweets_features)

    if flag_birthday:
        mask_wc_on_birthday = birthday_character['mask_wc_on_birthday']
        if mask_wc_on_birthday:
            generate_masked_wc(words, bucket, birthday_character)
        else:
            generate_wc(words, img_config, bucket)
    else:
        generate_wc(words, img_config, bucket)

    generate_sub_image(tweets_features, img_config)

    merge_image()
