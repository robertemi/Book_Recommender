import os, chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
from dotenv import load_dotenv


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma")


load_dotenv()
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("book_summaries")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

'''

Returns top k hits for the given user query

'''
def search_books(query: str, k: int = 3):
    
    embedded_query = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding
    
    res = collection.query(query_embeddings=[embedded_query], n_results=k)
    hits = []
    if res and res.get("ids"):
        for i in range(len(res["ids"][0])):
            hits.append({
                "title": res["metadatas"][0][i]["title"],
                "text": res["documents"][0][i],
            })
    return hits
