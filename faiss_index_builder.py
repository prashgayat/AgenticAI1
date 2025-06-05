# faiss_index_builder.py

from utils.retriever_utils import JobRetriever

def build_faiss_index_from_csv(csv_path="job_data.csv"):
    print("\n📦 Building FAISS index from CSV...")
    retriever = JobRetriever()
    retriever.main(csv_path)
    print("\n✅ FAISS index and metadata successfully created.")

def main():
    build_faiss_index_from_csv()

if __name__ == "__main__":
    main()
