import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

current_dir = Path(__file__).resolve().parent

file_path_robotics = current_dir / '../data/processed/Robotics_papers.csv'
file_path_nlp = current_dir / '../data/processed/Computation_and_Language_(Natural_Language_Processing)_papers.csv'

ready_dir = current_dir / '../data/ready'

df_robotics = pd.read_csv(file_path_robotics)
df_nlp = pd.read_csv(file_path_nlp)

robotics_len = len(df_robotics)
print(f"Target length based on Robotics dataset: {robotics_len} rows")

df_nlp_balanced = df_nlp.sample(n=robotics_len, random_state=42)

train_robo, test_robo = train_test_split(df_robotics, test_size=0.2, random_state=42)
train_nlp, test_nlp = train_test_split(df_nlp_balanced, test_size=0.2, random_state=42)

train_robo.to_csv(ready_dir / 'train_robotics.csv', index=False)
test_robo.to_csv(ready_dir / 'test_robotics.csv', index=False)

train_nlp.to_csv(ready_dir / 'train_nlp.csv', index=False)
test_nlp.to_csv(ready_dir / 'test_nlp.csv', index=False)

print("Datasets balanced, split, and successfully saved to data/ready!")