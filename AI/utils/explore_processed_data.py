import pandas as pd
from pathlib import Path


current_dir = Path(__file__).resolve().parent

file_path_robotics = current_dir / '../data/processed/Robotics_papers.csv'
file_path_nlp = current_dir / '../data/processed/Computation_and_Language_(Natural_Language_Processing)_papers.csv'

df_robotics = pd.read_csv(file_path_robotics)
df_nlp = pd.read_csv(file_path_nlp)

print("Robotics papers:")
print(df_robotics.shape[0])
print("\n")
print(df_robotics.head())
print("\n")
print(df_robotics.describe())
print("NLP papers:")
print(df_nlp.shape[0])
print("\n")
print(df_nlp.head())
print("\n")
print(df_nlp.describe())
