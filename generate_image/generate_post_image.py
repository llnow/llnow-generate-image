from generate_wc import *
from generate_sub_image import *
from merge_image import *


def generate_post_image(words, bucket):
    generate_wc(words, bucket)
    generate_sub_image()
    merge_image()
