import matplotlib.pyplot as plt

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

def pluralize(number, singular, plural):
     if number <= 1:
         return singular
     else:
         return plural

def save_donut_chart(ax, filename):
    ax.pie([1], radius=0.6, colors=['white'])
    plt.savefig(filename, bbox_inches='tight')

def human_join(list):
    str = ''

    for i, item in enumerate(list):
        if str != '':
            if i < len(list) - 1:
                str += ', '
            else:
                str += ' et '

        str += item

    return str
