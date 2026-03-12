import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# load vector index
index = faiss.read_index("rag/car_index.faiss")

# load stored chunks
chunks = np.load("rag/car_chunks.npy", allow_pickle=True)


def retrieve_cars(query, k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results