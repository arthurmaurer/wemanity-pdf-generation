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

def format_number(number):
    number = round(number, 2)
    return '{:,}'.format(number).replace(',', ' ')
