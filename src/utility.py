def escape_variables(variables):
    for key, value in variables.items():
        if type(value) == str:
            variables[key] = escape_latex(value)

    return variables

def escape_latex(value):
    return value \
        .replace('_', '\\_') \
        .replace('{', '\\{') \
        .replace('}', '\\}')

def format_number(number, decimals = 0):
    number = round(number, decimals)
    str = '{:,}'.format(number).replace(',', ' ')

    parts = str.split('.')

    if (decimals == 0):
        return parts[0]

    if len(parts) == 1:
        parts.append('0' * decimals)
    elif len(parts[1]) < decimals:
        parts[1] += '0' * (decimals - len(parts[1]))

    return '.'.join(parts)
