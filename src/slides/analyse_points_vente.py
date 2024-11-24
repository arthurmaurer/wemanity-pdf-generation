import math
import pandas as pd
import matplotlib.pyplot as plt

def generate(context, df):
    max_par_graph = 3
    nb_graphs = math.ceil(context['ca_magasins'].shape[0] / max_par_graph)

    for graph_i in range(nb_graphs):
        values = []
        labels = []

        for i in range(max_par_graph):
            i += graph_i * max_par_graph

            if i < context['ca_magasins'].shape[0]:
                values.append(context['ca_magasins'].loc[i]['ca'])
                labels.append(context['ca_magasins'].loc[i]['nom_magasin'])
            else:
                values.append(0)
                labels.append(f'_ {i}')

        graph_df = pd.DataFrame({'value': values, 'labels': labels})
        fig, ax = plt.subplots()
        graph_df.plot.bar(ax=ax, y='value', x='labels')

        filename = f'assets/ca_{graph_i}.jpg'
        plt.savefig(filename, bbox_inches='tight')
        context['assets']['ca'].append(filename)
