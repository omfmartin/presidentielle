import numpy as np
import pandas as pd
import json
import pickle

def format_results_bureau_de_vote(raw_df):

    df = raw_df.copy()

    # Extract number of votes per candidate and format to DataFrame
    start_candidates = np.where(raw_df.columns.str.match(pat=r'^N°Panneau$'))[
        0][0].astype(int)
    end_candidates = raw_df.shape[1]
    step = 7
    n_candidates = ((end_candidates - start_candidates) / step).astype(int)

    voix_df = []
    s = start_candidates
    for i in range(n_candidates):

        e = s+step
        res = raw_df.iloc[:, s:e].copy()

        # retrieve and format candidate's last name
        nom = res.iloc[0, 2]
        nom = nom.replace(" ", "_")
        nom = nom.replace("-", "_")
        nom = '_'.join([x.capitalize() for x in nom.split("_")])
        nom = nom.replace("é", "e")

        # number of votes for candidate
        voix = res.iloc[:, 4]

        # format to DataFrame
        out = pd.DataFrame(voix)
        out.columns = [nom]
        voix_df.append(out)
        s = e

    voix_df = pd.concat(voix_df, axis=1)

    # Rename columns, drop useless columns and append formated votes
    # We won't distinguish blank, invalid ballots and not casting a ballot
    df = df.iloc[:, :start_candidates]
    df = df.drop(columns=[x for x in df.columns if x.startswith('%')])
    df['No_One'] = df['Abstentions'] + df['Blancs'] + df['Nuls']

    df = df.rename(columns={
        'Code du département': 'CodeDepartement',
        'Libellé du département': 'NomDepartement',
        'Code de la circonscription': 'CodeCirconscription',
        'Libellé de la circonscription': 'NomCirconscription',
        'Code de la commune': 'CodeCommune',
        'Libellé de la commune': 'NomCommune',
        'Code du b.vote':  'CodeBureauVote'})

    # for col in ['CodeDepartement', 'NomDepartement', 'NomCirconscription', 'NomCommune']:
    #     df[col] = df[col].astype('category')

    df = pd.concat([df, voix_df], axis=1)

    return df

def filter_results_bureau_de_vote(df1, df2):

    filt_df1 = df1.copy()
    filt_df2 = df2.copy()

    mask = ((df1["Votants"] - df1["No_One"] >= 30) & 
        (df2["Votants"] - df2["No_One"] >= 30))

    filt_df1 = df1.loc[mask, :].reset_index(drop=True)
    filt_df2 = df2.loc[mask, :].reset_index(drop=True)

    return filt_df1, filt_df2

def compute_proportion_of_votes(df, columns):
    prop = df.loc[:,columns]
    prop = prop.apply(lambda x: x / df["Inscrits"], axis=0)
    return prop

# Main ----
with open("./raw_data/columns.json") as f:
    colnames = json.load(f)

print("Formatting first round")
raw_df1 = pd.read_excel(
    "./raw_data/resultats-par-niveau-burvot-t1-france-entiere.xlsx")
full_df1 = format_results_bureau_de_vote(raw_df1)

print("Formatting second round")
raw_df2 = pd.read_excel(
    "./raw_data/resultats-par-niveau-burvot-t2-france-entiere.xlsx")
full_df2 = format_results_bureau_de_vote(raw_df2)

print("Filtering results")
df1, df2 = filter_results_bureau_de_vote(full_df1, full_df2)

print('Computing proportions')
prop1 = compute_proportion_of_votes(df1, colnames.get('choices1'))
prop2 = compute_proportion_of_votes(df2, colnames.get('choices2'))

print("Saving results")
out = {
    'colnames': colnames,
    'full_df1': full_df1,
    'full_df2': full_df2,
    'df1': df1,
    'df2': df2,
    'prop1': prop1,
    'prop2': prop2
}
with open('./data/presidentielle.pkl', 'wb') as f:
    pickle.dump(file=f, obj=out)

print("Done!")
