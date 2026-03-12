import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load dataset
df = pd.read_csv("../data/cars.csv")

# Create chunks
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

print("Chunks created:", len(chunks))


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(chunks)

print("Embedding shape:", embeddings.shape)


# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

print("Vectors stored in FAISS:", index.ntotal)


# Save index
faiss.write_index(index, "car_index.faiss")

# Save chunks
np.save("car_chunks.npy", chunks)

print("Vector database saved successfully")