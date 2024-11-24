import matplotlib.pyplot as plt
import utility

def generate(context, df):
    df_localisation = df.groupby('localisation')['ca'].sum()
    context['ca_par_localisation'] = df_localisation / df_localisation.sum() * 100

    fig, ax = plt.subplots()
    labels = []

    for localisation, part_ca in context['ca_par_localisation'].items():
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
