import pandas as pd

# Load dataset
df = pd.read_csv("../data/cars.csv")

chunks = []

for _, row in df.iterrows():

    text = f"""
    Car Name: {row['name']}
    Fuel Type: {row['fuel']}
    Vehicle Type: {row['type']}
    Price: {row['price']}
    Mileage: {row['mileage']} kmpl
    Transmission: {row['transmission']}
    Description: {row['description']}
    """

    chunks.append(text.strip())

print("Total chunks:", len(chunks))
print("\nExample chunk:\n")
print(chunks[0])