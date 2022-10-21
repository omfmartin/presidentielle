import numpy as np
import pandas as pd

def format_results_bureau_de_vote(filename):
    raw_df = pd.read_excel(filename)

    ## Extract number of votes per candidate and format to DataFrame
    start_candidates = np.where(raw_df.columns.str.match(pat=r'^N°Panneau$'))[0][0].astype(int)
    end_candidates = raw_df.shape[1]
    step = 7
    n_candidates = ((end_candidates - start_candidates) / 7).astype(int)

    voix_df = []
    s = start_candidates
    for i in range(n_candidates):

        e = s+step
        res = raw_df.iloc[:,s:e].copy()

        # retrieve and format candidate's last name
        nom = res.iloc[0,2]
        nom = nom.replace(" ", "_")
        nom = nom.replace("-", "_")
        nom = '_'.join([x.capitalize() for x in nom.split("_")])
        nom = nom.replace("é", "e")

        # number of votes for candidate
        voix = res.iloc[:,4]

        # format to DataFrame 
        out = pd.DataFrame(voix)
        out.columns = [nom]
        voix_df.append(out)
        s = e

    voix_df = pd.concat(voix_df, axis=1)

    ## Rename columns, drop useless columns and append formated votes
    # We won't distinguish blank, invalid ballots and not casting a ballot
    df = raw_df.copy()
    df = df.iloc[:,:start_candidates]
    df['No_One'] = df['Abstentions'] + df['Blancs'] + df['Nuls']
    df = df.drop(columns=[x for x in df.columns if x.startswith('%')])
    df = pd.concat([df, voix_df], axis=1)
    df = df.rename(columns={
        'Code du département': 'CodeDepartement',
        'Libellé du département': 'NomDepartement',
        'Code de la circonscription': 'CodeCirconscription',
        'Libellé de la circonscription' : 'NomCirconscription',
        'Code de la commune': 'CodeCommune',
        'Libellé de la commune': 'NomCommune', 
        'Code du b.vote':  'CodeBureauVote'})

    return df

print("Formatting first round")
df1 = format_results_bureau_de_vote("./raw_data/resultats-par-niveau-burvot-t1-france-entiere.xlsx")
df1.to_csv("./data/presidentielle_t1.csv", index=False)

print("Formatting second round")
df2 = format_results_bureau_de_vote("./raw_data/resultats-par-niveau-burvot-t2-france-entiere.xlsx")
df2.to_csv("./data/presidentielle_t2.csv", index=False)

print("Done!")
