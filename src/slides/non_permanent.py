import matplotlib.pyplot as plt

def generate(context, df):
    context['non_permanent'] = {
        'ca_total': None,
        'part_ca_total': None,
        'ca_par_magasin': None,
        'magasin_plus_gros_ca': None,
        'magasins_sans_non_permanent': None,
    }
    sub_context = context['non_permanent']

    #--

    df_non_permanent = df[df['mode_de_gestion'] == 'NON PERMANENT']

    sub_context['ca_total'] = df_non_permanent['ca'].sum()
    sub_context['part_ca_total'] = sub_context['ca_total'] / df['ca'].sum() * 100

    #--

    ca_par_magasin = df_non_permanent \
        .groupby('nom_magasin')['ca'] \
        .sum() \
        .sort_values(ascending=False)

    sub_context['ca_par_magasin'] = ca_par_magasin

    #--

    sub_context['magasin_plus_gros_ca'] = {
       'nom': ca_par_magasin.index[0],
       'ca': ca_par_magasin.iloc[0],
       'part_ca': ca_par_magasin.iloc[0] / sub_context['ca_total'] * 100,
    }

    #--

    sub_context['magasins_sans_non_permanent'] = []
    df_modes_gestion = df.groupby(['nom_magasin', 'mode_de_gestion'])['ca'].sum()

    ca_magasins = {}

    for indices, ca in df_modes_gestion.items():
        nom_magasin, mode = indices

        if nom_magasin not in ca_magasins:
            ca_magasins[nom_magasin] = {
                'PERMANENT': 0,
                'NON PERMANENT': 0,
            }

        ca_magasins[nom_magasin][mode] = ca

    sub_context['magasins_sans_non_permanent'] = []

    for nom_magasin, modes in ca_magasins.items():
        if modes['NON PERMANENT'] == 0 and modes['PERMANENT'] != 0:
            sub_context['magasins_sans_non_permanent'].append(nom_magasin)

    #--

    fig, ax = plt.subplots()
    ca_par_magasin.plot.bar(
        ax=ax,
        title='CA NON PERMANENT par magasin',
        ylabel='',
        xlabel='',
    )

    filename = f'assets/__ca_non_permanent_par_magasin.jpg'
    plt.savefig(filename, bbox_inches='tight')
