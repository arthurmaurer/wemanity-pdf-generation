import matplotlib.pyplot as plt
import numpy as np
import utility
from pprint import pprint

def generate(context, df):
    magasins = {}
    context['part_ca_mode_permanent'] = 0
    context['part_ca_mode_non_permanent'] = 0
    context['ca_mode_permanent'] = 0
    context['ca_mode_non_permanent'] = 0
    total = 0

    for i, row in df.iterrows():
        nom_magasin = row['nom_magasin']
        ca = row['ca']

        if nom_magasin not in magasins:
            magasins[nom_magasin] = {
                'permanent': 0,
                'non_permanent': 0,
                'total': 0,
            }

        if row['mode_de_gestion'] == 'PERMANENT':
            context['ca_mode_permanent'] += ca
            magasins[nom_magasin]['permanent'] += ca

        if row['mode_de_gestion'] == 'NON PERMANENT':
            context['ca_mode_non_permanent'] += ca
            magasins[nom_magasin]['non_permanent'] += ca

        magasins[nom_magasin]['total'] += ca
        total += ca

    context['part_ca_mode_permanent'] = context['ca_mode_permanent'] / total * 100
    context['part_ca_mode_non_permanent'] = context['ca_mode_non_permanent'] / total * 100

    context['magasins_permanents_seulement'] = []

    for nom_magasin, magasin in magasins.items():
        if magasin['total'] > 0 and magasin['non_permanent'] == 0:
            context['magasins_permanents_seulement'].append(nom_magasin)

    #-- Graphique CA total

    df_ca_par_mode_gestion = df.groupby(['magasin', 'mode_de_gestion'])['ca'].sum()
    context['ca_par_mode_de_gestion_par_magasin'] = df_ca_par_mode_gestion.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))

    df_ca_par_mode_gestion = df.groupby('mode_de_gestion')['ca'].sum()
    context['ca_par_mode_de_gestion'] = df_ca_par_mode_gestion / df_ca_par_mode_gestion.sum() * 100

    fig, ax = plt.subplots()
    ax.set_title('Part de CA par mode de gestion')
    labels = ['Permanent', 'Non permanent']
    values = [
        context['part_ca_mode_permanent'],
        context['part_ca_mode_non_permanent'],
    ]

    ax.pie(values, labels=labels)

    utility.save_donut_chart(ax, filename=f'assets/__ca_total_par_mode_de_gestion.jpg')


    #-- Graphique CA par magasin

    labels = []
    valeurs_permanent = []
    valeurs_non_permanent = []

    for nom_magasin, magasin in magasins.items():
        labels.append(nom_magasin)

        valeurs_permanent.append(magasin['permanent'] / magasin['total'] * 100)
        valeurs_non_permanent.append(magasin['non_permanent'] / magasin['total'] * 100)

    x = np.arange(len(magasins))
    width = 0.4

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    ax.set_ylabel('Part du CA')
    ax.set_title('CA par mode de gestion')
    ax.set_xticks(x)
    ax.set_xticklabels(magasins.keys())
    ax.set_ylim(0, 110)

    ax.bar(x - width / 2, valeurs_permanent, width, label='Permanent')
    ax.bar(x + width / 2, valeurs_non_permanent, width, label='Non permanent')

    for i, valeur in enumerate(valeurs_permanent):
        ax.annotate(
            '{}%'.format(utility.format_number(valeur)),
            xy=(i - width / 2, valeur),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center',
            va='bottom',
        )

    for i, valeur in enumerate(valeurs_non_permanent):
        ax.annotate(
            '{}%'.format(utility.format_number(valeur)),
            xy=(i + width / 2, valeur),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center',
            va='bottom',
        )

    ax.legend()

    filename = f'assets/__ca_magasins_par_mode_de_gestion.jpg'
    plt.savefig(filename, bbox_inches='tight')
