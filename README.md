# Présidentielle 2022

Analyses concerning the 2022 French presidential election.

## Description of Analyses

Jupyter notebooks are in `./notebooks/`.

#### exploration.ipynb

Presents the data and performs some EDA.

#### predicting_t1_to_t2.ipynb

Predicts second-round results from first-round results using a neural network.

## Reproduce Results

Before running Jupyter notebooks, please run these two functions to install packages and format data.

```
conda env create
python ./scripts/prepare_results.py
```

 ## Data Source

https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

https://www.data.gouv.fr/fr/datasets/geolocalisation-des-bureaux-de-vote/
