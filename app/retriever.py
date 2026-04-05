import os
import faiss
import numpy as np
from openai import OpenAI

client = OpenAI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICIES_DIR = os.path.join(BASE_DIR, "data")
CHUNK_SIZE = 250 #tokes (approximate - split by words)
CHUNK_OVERLAP = 50 # words of overlap between chunks


# Step 1: Load all policy files

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as f:
                text = f.read()
                documents.append({"source": filename, "text": text})
    return documents

#Step 2: Chunk each Document
def chunk_documents(doc, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = doc["text"].split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        chunks.append({
            "source": doc["source"],
            "chunk_id": len(chunks),
            "text": chunk_text,
        })
        start += chunk_size - overlap #slide forward with overlap
    return chunks

#Step 3: Embed a list of text strings

def embed_texts(texts):
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype="float32")

#Step 4: Build and return the FAISS index + chunk metadata

def build_index(policies_dir=POLICIES_DIR):
    #Load
    documents = load_documents(policies_dir)

    #Chunk
    all_chunks =[]
    for doc in documents:
        all_chunks.extend(chunk_documents(doc))

    print(f"Total chunks: {len(all_chunks)}")

    #Embed
    texts = [chunk["text"] for chunk in all_chunks]
    vectors = embed_texts(texts)

    #index
    dimension = vectors.shape[1] #1536 for text-embedding-3-small
    index = faiss.IndexFlatIP(dimension) #Inner product = cosine sim on normalized

    #normalize vectors before adding (required for cosine similarity)
    faiss.normalize_L2(vectors)
    index.add(vectors)

    print(f"Index built. {index.ntotal} vector stored.")
    return index, all_chunks

#Step 5: Query the index

def retrieve(query, index, all_chunks, k=3):
    #embed the query
    query_vector = embed_texts([query])
    faiss.normalize_L2(query_vector)

    #search
    scores, indices = index.search(query_vector, k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "text": all_chunks[idx]["text"],
            "source": all_chunks[idx]["source"],
            "chunk_id": all_chunks[idx]["chunk_id"],
            "score": float(score)
        })
    return results

