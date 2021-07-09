import os


def config_img():
    img_width = int(os.environ['IMG_WIDTH'])
    wc_height = int(os.environ['WC_HEIGHT'])
    sub_img_height = int(os.environ['SUB_IMG_HEIGHT'])
    sub_img_left_margin = int(os.environ['SUB_IMG_LEFT_MARGIN'])
    sub_img_right_margin = int(os.environ['SUB_IMG_RIGHT_MARGIN'])
    sub_img_above_font_size = int(os.environ['SUB_IMG_ABOVE_FONT_SIZE'])
    sub_img_below_font_size = int(os.environ['SUB_IMG_BELOW_FONT_SIZE'])
    sub_img_bg_color = os.environ['SUB_IMG_BG_COLOR']
    img_config = {
        'img_width': img_width,
        'wc_height': wc_height,
        'sub_img_height': sub_img_height,
        'sub_img_left_margin': sub_img_left_margin,
        'sub_img_right_margin': sub_img_right_margin,
        'sub_img_above_font_size': sub_img_above_font_size,
        'sub_img_below_font_size': sub_img_below_font_size,
        'sub_img_bg_color': sub_img_bg_color
    }

    return img_config
