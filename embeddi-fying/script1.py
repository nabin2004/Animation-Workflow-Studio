import os
import ast
import json

def extract_code_chunks(base_dir, output_path="manim_code_chunks.json"):
    chunks = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        source = file.read()
                    tree = ast.parse(source)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            start = node.lineno - 1
                            end = getattr(node, "end_lineno", start + 1)
                            code_chunk = "\n".join(source.splitlines()[start:end])
                            chunks.append({
                                "file": path,
                                "type": type(node).__name__,
                                "name": node.name,
                                "code": code_chunk
                            })
                except Exception as e:
                    print(f"[WARN] Skipped {path}: {e}")
    
    # Save the extracted chunks to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Extracted {len(chunks)} code chunks from {base_dir}")
    print(f"💾 Saved to {output_path}")
    print(f"Total chunks: {len(chunks)}")
    return chunks

if __name__ == "__main__":
    base_dir = "/home/nabin/Desktop/completeIt/manim/manim" 
    extract_code_chunks(base_dir)
