import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
DATA_PATH = os.path.join(BASE_DIR, "data", "books.txt")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma")
chromadb_client = chromadb.PersistentClient(path=CHROMA_DIR)

openai_client = OpenAI(api_key=api_key)
chromadb_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chromadb_client.get_or_create_collection("book_summaries")

def parse_books(path):
    books, title, summary = [], None, []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                ls = line.strip()
                if ls.lower().startswith('title'):
                    if title and summary:
                        books.append({"title": title, "text": "\n".join(summary).strip()})
                    title = line.split(":", 1)[1].strip()
                    summary = []
                else:
                    summary.append(line.rstrip("\n"))
        if title and summary:
            books.append({"title": title, "text": "\n".join(summary).strip()})
        return books
    except Exception as e:
        print(f'Error occured when parsing books: {e}')


def embedd_and_persist():
    books = parse_books(DATA_PATH)
    ids, documents, metadata, vectors = [], [], [], []
    try:
        for book in books:
            embedder = openai_client.embeddings.create(
                input=book['text'],
                model='text-embedding-3-small'
            )
            vector = embedder.data[0].embedding
            ids.append(re.sub(r"[^a-z0-9]+", "-", book["title"].lower()).strip("-"))
            documents.append(book["text"])
            metadata.append({"title": book["title"]})
            vectors.append(vector)

        collection.upsert(ids=ids, embeddings=vectors, documents=documents, metadatas=metadata)

    except Exception as e:
        print(f'Error occured when embedding/persisting to ChromaDB: {e}')


