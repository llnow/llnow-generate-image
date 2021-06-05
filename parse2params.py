def parse2params(parse_str, parse=None):
    if parse is None:
        parse = '&'
    return_params = {}
    parsed_str = parse_str.split(parse)
    for param_string in parsed_str:
        param, value = param_string.split('=', 1)
        return_params[param] = value
    return return_params
