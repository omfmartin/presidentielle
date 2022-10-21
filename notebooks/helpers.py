def compute_proportion_of_votes(df, columns):
    prop = df.loc[:,columns]
    prop = prop.apply(lambda x: x / df["Inscrits"], axis=0)
    return prop
