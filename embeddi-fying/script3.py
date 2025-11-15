import json
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("google/embeddinggemma-300m")  # use a working model
print("✅ Loaded embedding model.")

# Load embedded chunks
with open("manim_code_embedded.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"✅ Loaded {len(chunks)} embedded code chunks.")

# Convert embeddings to tensor (float32)
embeddings = torch.tensor(np.array([c["embedding"] for c in chunks]), dtype=torch.float32)

print("✅ Converted embeddings to tensor.")

# ---- Query Section ----
query = "create a circle"
query_embedding = model.encode(query, convert_to_tensor=True).to(torch.float32)
print("✅ Computed query embedding.")

# Compute cosine similarities
cosine_scores = util.cos_sim(query_embedding, embeddings)[0].cpu().numpy()
print("✅ Computed cosine similarities.")

# Get top-k results
top_k = 5
top_indices = np.argsort(-cosine_scores)[:top_k]


print(f"🔍 Top {top_k} code chunks for query: '{query}'\n")
for i in top_indices:
    c = chunks[i]
    print(f"📄 File: {c['file']}")
    print(f"🏷 Type: {c['type']} | Name: {c['name']}")
    print(f"💡 Similarity: {cosine_scores[i]:.4f}")
    print(f"```python\n{c['code'][:500]}...\n```\n{'-'*80}")
