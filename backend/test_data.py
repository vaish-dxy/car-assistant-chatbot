import pandas as pd

df = pd.read_csv("data/cars.csv")

print(df.head())
print("Total cars:", len(df))