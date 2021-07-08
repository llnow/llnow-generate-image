from PIL import Image


def merge_image():
    wc = Image.open('/tmp/wc.png')
    sub_img = Image.open('/tmp/sub_image.png')
    dst = Image.new('RGB', (wc.width, wc.height + sub_img.height))
    dst.paste(wc, (0, 0))
    dst.paste(sub_img, (0, wc.height))
    dst.save('/tmp/post_image.png')
