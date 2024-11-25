import csv
import jinja2
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import math
import utility
import pretty_errors
import os

context = dict(
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

    part_ca_mode_permanent = None,
    part_ca_mode_non_permanent = None,
    nb_magasins_permanent_uniquement = None,

    assets = dict(
        ca = [],
    ),
)


# -------------------
current_dir = os.path.dirname(os.path.realpath(__file__))

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(searchpath = f'{current_dir}/../template'),
    autoescape = jinja2.select_autoescape(),
    trim_blocks = True,
    variable_start_string = '<<',
    variable_end_string = '>>',
    block_start_string = '<@',
    block_end_string = '@>',
)

env.filters['number'] = utility.format_number
env.filters['human_join'] = utility.human_join
env.globals['pluralize'] = utility.pluralize

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

import slides.introduction
slides.introduction.generate(context, df)

import slides.analyse_points_vente
slides.analyse_points_vente.generate(context, df)

import slides.localisation
slides.localisation.generate(context, df)

import slides.activite
slides.activite.generate(context, df)

import slides.analyse_mode_gestion
slides.analyse_mode_gestion.generate(context, df)

import slides.non_permanent
slides.non_permanent.generate(context, df)

import slides.permanent
slides.permanent.generate(context, df)

#-- Generating the template


context = utility.escape_variables(context)

template = env.get_template('rapport.tex')
latex = template.render(**context)

print(latex)
