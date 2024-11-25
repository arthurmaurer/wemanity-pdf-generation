import matplotlib.pyplot as plt

def generate(context, df):
    context['permanent'] = {
        'ca_total': None,
        'part_ca_total': None,
        'ca_par_magasin': None,
        'magasin_plus_gros_ca': None,
    }
    sub_context = context['permanent']

    df_permanent = df[df['mode_de_gestion'] == 'PERMANENT']

    sub_context['ca_total'] = df_permanent['ca'].sum()
    sub_context['part_ca_total'] = sub_context['ca_total'] / df['ca'].sum() * 100

    ca_par_magasin = df_permanent \
        .groupby('nom_magasin')['ca'] \
        .sum() \
        .sort_values(ascending=False)

    sub_context['ca_par_magasin'] = ca_par_magasin

    sub_context['magasin_plus_gros_ca'] = {
       'nom': ca_par_magasin.index[0],
       'ca': ca_par_magasin.iloc[0],
       'part_ca': ca_par_magasin.iloc[0] / sub_context['ca_total'] * 100,
   }

    fig, ax = plt.subplots()
    ca_par_magasin.plot.bar(
        ax=ax,
        title='CA PERMANENT par magasin',
        ylabel='',
        xlabel='',
    )

    filename = f'assets/__ca_permanent_par_magasin.jpg'
    plt.savefig(filename, bbox_inches='tight')
