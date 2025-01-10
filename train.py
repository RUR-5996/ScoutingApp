import os
import pandas as pd
from sklearn.linear_model import ElasticNet

filedir = os.getcwd()

results = pd.read_csv(f"{filedir}/data/results.csv")

