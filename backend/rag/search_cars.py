import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("car_index.faiss")

# Load stored chunks
chunks = np.load("car_chunks.npy", allow_pickle=True)


def search(query, k=3):

    # convert query → embedding
    query_embedding = model.encode([query])

    # search FAISS
    distances, indices = index.search(np.array(query_embedding), k)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


# ------------------------
# Test the search
# ------------------------

query = "SUV under 15 lakh"

print("\nUser Query:", query)

results = search(query)

print("\nTop Matching Cars:\n")

for r in results:
    print(r)
    print("-------------")