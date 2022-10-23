import tensorflow as tf
import pandas as pd
import pickle
from helpers import create_model

with open('./data/presidentielle.pkl', 'rb') as f:
    data = pickle.load(f)

prop1 = data['prop1']
prop2 = data['prop2']

del data

model = create_model(
    input_shape=prop1.shape[1],
    output_shape=prop2.shape[1],
    hidden_shape=30,
    hidden_n_layers=2,
    batch_norm=False)
    
history = model.fit(
    x=prop1, 
    y=prop2,
    epochs=50, 
    validation_split=.1,
    verbose=1)

pd.DataFrame(history.history).plot(figsize=(8, 5))

model.save('./models/prop1_to_prop2')
