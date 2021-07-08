import os


def config_img():
    img_width = int(os.environ['IMG_WIDTH'])
    wc_height = int(os.environ['WC_HEIGHT'])
    sub_img_height = int(os.environ['SUB_IMG_HEIGHT'])
    sub_img_side_margin = int(os.environ['SUB_IMG_SIDE_MARGIN'])
    tweet_range_left_margin = int(os.environ['TWEET_RANGE_LEFT_MARGIN'])
    img_config = {
        'img_width': img_width,
        'wc_height': wc_height,
        'sub_img_height': sub_img_height,
        'sub_img_side_margin': sub_img_side_margin,
        'tweet_range_left_margin': tweet_range_left_margin
    }

    return img_config
