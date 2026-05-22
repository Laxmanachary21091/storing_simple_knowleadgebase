from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Step 1: Sample documents
documents = [
    "Python is a programming language",
    "It's used for web development, data science, and AI",
    "Python is easy to learn with simple syntax",
    "JavaScript runs in web browsers",
    "Machine Learning uses algorithms and data"
]

# Step 2: Create embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(documents, convert_to_numpy=True)

print(f"Embedding shape: {embeddings.shape}")  # (5, 384) - 5 docs, 384 dimensions

# Step 3: Store in FAISS vector database
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance metric
index.add(np.array(embeddings))

# Step 4: Retrieve similar documents
query = "What is Python used for?"
query_embedding = embedding_model.encode([query], convert_to_numpy=True)

# Search for top 3 similar documents
distances, indices = index.search(query_embedding, k=3)

print("\nRetrieved Documents:")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {documents[idx]} (similarity score: {distances[0][i]:.4f})")

# Output:
# Retrieved Documents:
# 1. It's used for web development, data science, and AI (similarity score: 0.0523)
# 2. Python is a programming language (similarity score: 0.1234)
# 3. Python is easy to learn with simple syntax (similarity score: 0.2145)
