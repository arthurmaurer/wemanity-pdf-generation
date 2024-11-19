import csv
import jinja2
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import math
import utility


variables = dict(
    fournisseur = 'ABC',
    periode = 'Avril à Juin',
    annee = 2024,
    ca_mois = 123456,
    nb_uvc_mois = 123,
    nb_ref_mois = 123,
    nb_magasin = 123,
    list_mag_nop = ['A', 'B', 'C'],
    nom_contrat = 'ABC',
    date_contrat = '11 mars 2024',

    magasin_ca_plus_eleve = None,
    magasin_ca_moins_eleve = None,
    magasin_uvc_plus_eleve = None,
    magasin_uvc_moins_eleve = None,

    assets = dict(
        ca = [],
    ),
)



# -------------------

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(searchpath = './'),
    autoescape = jinja2.select_autoescape(),
    trim_blocks = True,
    variable_start_string = '<<',
    variable_end_string = '>>',
    block_start_string = '<@',
    block_end_string = '@>',
)

env.filters['number'] = utility.format_number


# -------------------

df = pd.read_csv(
    './data/CM2_2.csv',
    sep=';',
    names=['magasin', 'nom_magasin', 'activite', 'localisation', 'code_accord', 'libelle_fournisseur', 'mode_de_gestion', 'article', 'libelle_article', 'ca', 'quantite'],
    skiprows=1,
)

df['ca'] = df['ca'].str.replace(',', '.').astype('float')

# print(df)

ca_magasins = df.groupby(['magasin', 'nom_magasin'], as_index=False)['ca'].sum()

uvc_magasins = df.groupby(['nom_magasin'])['quantite'].sum()
variables['magasin_ca_plus_eleve'] = ca_magasins.loc[ca_magasins['ca'].idxmax()]
variables['magasin_ca_moins_eleve'] = ca_magasins.loc[ca_magasins['ca'].idxmin()]

uvc_magasins = df.groupby(['magasin', 'nom_magasin'], as_index=False)['quantite'].sum()
variables['magasin_uvc_plus_eleve'] = uvc_magasins.loc[uvc_magasins['quantite'].idxmax()]
variables['magasin_uvc_moins_eleve'] = uvc_magasins.loc[uvc_magasins['quantite'].idxmin()]

magasins = {}

with open('data/CM2_2.csv', newline='') as file:
    reader = csv.reader(file, delimiter = ';', quotechar = '|')

    for i, row in enumerate(reader):
        if i == 0:
            continue

        magasin = row[0]
        nom_magasin = row[1]
        ca = float(row[9].replace(',', '.'))
        quantite = int(row[10])

        if magasin not in magasins:
            magasins[magasin] = dict(
                id = magasin,
                nom = nom_magasin,
                ca = 0,
                uvc = 0,
            )

        magasins[magasin]['ca'] = magasins[magasin]['ca'] + ca
        magasins[magasin]['uvc'] = magasins[magasin]['uvc'] + quantite

# pprint(variables, file=sys.stderr)

max_par_graph = 3

nb_graphs = math.ceil(ca_magasins.shape[0] / max_par_graph)

for graph_i in range(nb_graphs):
    values = []
    labels = []
    colors = []

    for i in range(max_par_graph):
        i += graph_i * max_par_graph

        if i < ca_magasins.shape[0]:
            values.append(ca_magasins.loc[i]['ca'])
            labels.append(ca_magasins.loc[i]['nom_magasin'])
        else:
            values.append(0)
            labels.append(f'_ {i}')

    df = pd.DataFrame({'value': values, 'labels': labels})
    fig, ax = plt.subplots()
    df.plot.bar(ax=ax, y='value', x='labels')

    filename = f'assets/ca_{graph_i}.jpg'
    plt.savefig(filename, bbox_inches='tight')
    variables['assets']['ca'].append(filename)

variables = utility.escape_variables(variables)

template = env.get_template('jinja2_template.tex')
latex = template.render(**variables)

print(latex)
