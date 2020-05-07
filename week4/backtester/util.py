import re
def parse_symbol(symbol):
    result = re.match(r'^(.*)\d{4}$', symbol)
    if result is not None:
        return result[1]
    else:
        return symbol
