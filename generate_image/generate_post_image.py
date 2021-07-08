from generate_wc import *
from generate_sub_image import *
from merge_image import *


def generate_post_image(words, img_config, bucket):
    generate_wc(words, img_config, bucket)
    generate_sub_image(img_config)
    merge_image()
