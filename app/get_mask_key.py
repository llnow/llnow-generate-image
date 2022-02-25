import sys


def get_birthday_character_mask_key(birthday_character):
    series = birthday_character['series']
    first_name_en = birthday_character['first_name_en']
    mask_key = 'mask/LL-icon-mask/{}_icon/{}.png'.format(series, first_name_en)

    return mask_key


def get_special_mask_key(img_basename):
    mask_key = 'mask/special/{}.png'.format(img_basename)

    return mask_key


def get_mask_key(mask_type, mask_requirements):
    if mask_type == 'birthday_character':
        mask_key = get_birthday_character_mask_key(birthday_character=mask_requirements)
    elif mask_type == 'special':
        mask_key = get_special_mask_key(img_basename=mask_requirements)
    else:
        sys.exit('unknown mask_type')

    return mask_key
