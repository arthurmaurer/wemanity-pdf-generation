import matplotlib.pyplot as plt
import utility

def generate(context, df):
    df_activite = df.groupby('activite')['ca'].sum()
    context['df_activite'] = df_activite
    context['ca_par_activite'] = df_activite / df_activite.sum() * 100

    fig, ax = plt.subplots()
    labels = []

    for localisation, part_ca in context['ca_par_activite'].items():
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
