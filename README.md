# Présidentielle 2022

Analyses concerning the 2022 French presidential election.

## Description of Analyses

Jupyter notebooks are in `./notebooks/`.

#### exploration.ipynb

Presents the data and performs some EDA.

#### model_selection.ipynb

Selecting neural network architecture using cross-validation.

#### predict_2nd_from_1st_round.ipynb

Predicts second-round results from first-round results using a neural network.

## Reproduce Results

Before running Jupyter notebooks, please run these two functions to install packages and format data.

```
conda env create
python ./scripts/prepare_results.py
python ./scripts/fit_models.py
```

 ## Data Source

https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

https://www.data.gouv.fr/fr/datasets/geolocalisation-des-bureaux-de-vote/
