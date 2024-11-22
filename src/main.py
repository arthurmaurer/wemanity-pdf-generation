import csv
import jinja2
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import utility


variables = dict(
    fournisseur = 'Fournisseur ABC',
    periode = 'Avril à Juin',
    annee = 2024,
    ca_total_mois = None,
    nb_uvc_mois = None,
    nb_ref_mois = None,
    nb_magasins = None,
    list_mag_nop = ['A', 'B', 'C'],
    nom_contrat = 'Contrat ABC',
    date_contrat = '11 mars 2024',

    magasin_ca_plus_eleve = None,
    magasin_ca_moins_eleve = None,
    magasin_uvc_plus_eleve = None,
    magasin_uvc_moins_eleve = None,

    ca_par_localisation = None,
    ca_par_activite = None,

    ca_par_mode_de_gestion = None,

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

if df.dtypes['ca'] == 'object':
    df['ca'] = df['ca'].str.replace(',', '.').astype('float')

# print(df)

variables['ca_total_mois'] = df['ca'].sum()
variables['nb_uvc_mois'] = df['quantite'].sum()
variables['nb_ref_mois'] = df['article'].nunique()
variables['nb_magasins'] = df['magasin'].nunique()

ca_magasins = df.groupby(['magasin', 'nom_magasin'], as_index=False)['ca'].sum()

uvc_magasins = df.groupby(['nom_magasin'])['quantite'].sum()
variables['magasin_ca_plus_eleve'] = ca_magasins.loc[ca_magasins['ca'].idxmax()]
variables['magasin_ca_moins_eleve'] = ca_magasins.loc[ca_magasins['ca'].idxmin()]

uvc_magasins = df.groupby(['magasin', 'nom_magasin'], as_index=False)['quantite'].sum()
variables['magasin_uvc_plus_eleve'] = uvc_magasins.loc[uvc_magasins['quantite'].idxmax()]
variables['magasin_uvc_moins_eleve'] = uvc_magasins.loc[uvc_magasins['quantite'].idxmin()]



#-- Generating the CA graphs

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

    graph_df = pd.DataFrame({'value': values, 'labels': labels})
    fig, ax = plt.subplots()
    graph_df.plot.bar(ax=ax, y='value', x='labels')

    filename = f'assets/ca_{graph_i}.jpg'
    plt.savefig(filename, bbox_inches='tight')
    variables['assets']['ca'].append(filename)



#-- Generating the localisation graph

df_localisation = df.groupby('localisation')['ca'].sum()
variables['ca_par_localisation'] = df_localisation / df_localisation.sum() * 100

fig, ax = plt.subplots()
labels = []

for localisation, part_ca in variables['ca_par_localisation'].items():
    part_ca = utility.format_number(part_ca, 1)
    labels.append(f"{localisation}\n{part_ca}%")

df_localisation.plot.pie(
    ax=ax,
    title='Part de CA par localisation',
    labels=labels,
    ylabel='',
)

ax.pie([1], radius=0.6, colors=['white'])

filename = f'assets/ca_par_localisation.jpg'
plt.savefig(filename, bbox_inches='tight')



#-- Generating the activity graph

df_activite = df.groupby('activite')['ca'].sum()
variables['ca_par_activite'] = df_activite / df_activite.sum() * 100

fig, ax = plt.subplots()
labels = []

for localisation, part_ca in variables['ca_par_activite'].items():
    part_ca = utility.format_number(part_ca, 1)
    labels.append(f"{localisation}\n{part_ca}%")

df_activite.plot.pie(
    ax=ax,
    title='Part de CA par activité',
    labels=labels,
    ylabel='',
)

ax.pie([1], radius=0.6, colors=['white'])

filename = f'assets/ca_par_activite.jpg'
plt.savefig(filename, bbox_inches='tight')



#-- Mode de gestion

df_ca_par_mode_gestion = df.groupby(['magasin', 'mode_de_gestion'])['ca'].sum()
variables['ca_par_mode_de_gestion_par_magasin'] = df_ca_par_mode_gestion.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))

df_ca_par_mode_gestion = df.groupby('mode_de_gestion')['ca'].sum()
variables['ca_par_mode_de_gestion'] = df_ca_par_mode_gestion / ca_par_mode_gestion.sum() * 100

fig, ax = plt.subplots()
labels = []

for mode_gestion, part_ca in variables['ca_par_mode_de_gestion_par_magasin'].items():
    part_ca = utility.format_number(part_ca, 1)
    labels.append(f"{mode_gestion}\n{part_ca}%")

df_activite.plot.pie(
    ax=ax,
    title='Part de CA par mode de gestion',
    labels=labels,
    ylabel='',
)

ax.pie([1], radius=0.6, colors=['white'])

filename = f'assets/ca_par_mode_de_gestion.jpg'
plt.savefig(filename, bbox_inches='tight')


#-- Generating the template


variables = utility.escape_variables(variables)

template = env.get_template('jinja2_template.tex')
latex = template.render(**variables)

print(latex)
