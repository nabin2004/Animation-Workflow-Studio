from sentence_transformers import SentenceTransformer
import json


# Download from the 🤗 Hub
model = SentenceTransformer("google/embeddinggemma-300m")

# from huggingface_hub import login
# login()

# model = SentenceTransformer("google/embedding-gemma-300m")

# Load chunks
with open("manim_code_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["code"] for c in chunks]

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model_id = "google/embeddinggemma-300m"
# # model = SentenceTransformer(model_id).to(device=device)

# model = SentenceTransformer("google/embeddinggemma-300m")

embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)

# Attach embeddings
for i, emb in enumerate(embeddings):
    chunks[i]["embedding"] = emb.tolist()

# Save embedded dataset
with open("manim_code_embedded.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("✅ Saved embedded chunks to manim_code_embedded.json")

