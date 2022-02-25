from read_tweets_features import *
from check_birthday import *
from check_special_mask import *
from generate_masked_wc import *
from generate_wc import *
from generate_sub_image import *
from merge_image import *


def generate_post_image(words, img_config, bucket):
    tweets_features = read_tweets_features(bucket)
    flag_birthday, birthday_character = check_birthday(tweets_features)
    flag_special_mask, img_basename = check_special_mask(tweets_features)

    if flag_special_mask:
        generate_masked_wc(words, mask_type='special', mask_requirements=img_basename)
    elif flag_birthday:
        mask_wc_on_birthday = birthday_character['mask_wc_on_birthday']
        if mask_wc_on_birthday:
            generate_masked_wc(words, mask_type='birthday_character', mask_requirements=birthday_character)
        else:
            generate_wc(words, img_config)
    else:
        generate_wc(words, img_config)

    generate_sub_image(tweets_features, img_config)

    merge_image()
