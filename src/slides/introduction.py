def generate(context, df):
    context['ca_total_mois'] = df['ca'].sum()
    context['nb_uvc_mois'] = df['quantite'].sum()
    context['nb_ref_mois'] = df['article'].nunique()
    context['nb_magasins'] = df['magasin'].nunique()

    ca_magasins = df.groupby(['magasin', 'nom_magasin'], as_index=False)['ca'].sum()
    context['ca_magasins'] = ca_magasins

    uvc_magasins = df.groupby(['nom_magasin'])['quantite'].sum()
    context['magasin_ca_plus_eleve'] = ca_magasins.loc[ca_magasins['ca'].idxmax()]
    context['magasin_ca_moins_eleve'] = ca_magasins.loc[ca_magasins['ca'].idxmin()]

    uvc_magasins = df.groupby(['magasin', 'nom_magasin'], as_index=False)['quantite'].sum()
    context['magasin_uvc_plus_eleve'] = uvc_magasins.loc[uvc_magasins['quantite'].idxmax()]
    context['magasin_uvc_moins_eleve'] = uvc_magasins.loc[uvc_magasins['quantite'].idxmin()]
