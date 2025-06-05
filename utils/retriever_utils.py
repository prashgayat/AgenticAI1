# retriever_utils.py (Refactored for FAISS Job Search)

import os
import faiss
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

class JobRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.dimension = None

    def build_index(self, descriptions):
        print("🔧 Creating embeddings for job descriptions...")
        embeddings = self.embedding_model.encode(descriptions, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')

        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        print(f"✅ FAISS index created with {len(descriptions)} vectors.")
        return self.index

    def save_index(self, path="faiss_index.idx"):
        if self.index is not None:
            faiss.write_index(self.index, path)
            print(f"💾 Saved FAISS index to {path}")

    def save_metadata(self, metadata, path="job_metadata.pkl"):
        with open(path, "wb") as f:
            pickle.dump(metadata, f)
            print(f"💾 Saved metadata to {path}")

    def main(self, csv_path="job_data.csv"):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"❌ job_data.csv not found at path: {csv_path}")

        df = pd.read_csv(csv_path)
        df.dropna(subset=["description"], inplace=True)
        descriptions = df["description"].tolist()

        self.build_index(descriptions)
        self.save_index("faiss_index.idx")
        self.save_metadata(df.to_dict(), "job_metadata.pkl")

if __name__ == "__main__":
    retriever = JobRetriever()
    retriever.main()
