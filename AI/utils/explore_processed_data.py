import pandas as pd
from pathlib import Path

def explore_dataframe(df, dataset_name):
    print(f"\n{dataset_name}")
    print(f"Shape: {df.shape}")
    print(df.head())
    df.info()
    print(df.describe())

current_dir = Path(__file__).resolve().parent
ready_dir = current_dir / '../data/ready'

train_robotics = pd.read_csv(ready_dir / 'train_robotics.csv')
test_robotics = pd.read_csv(ready_dir / 'test_robotics.csv')
train_nlp = pd.read_csv(ready_dir / 'train_nlp.csv')
test_nlp = pd.read_csv(ready_dir / 'test_nlp.csv')

explore_dataframe(train_robotics, "TRAIN - Robotics")
explore_dataframe(test_robotics, "TEST - Robotics")
explore_dataframe(train_nlp, "TRAIN - NLP")
explore_dataframe(test_nlp, "TEST - NLP")