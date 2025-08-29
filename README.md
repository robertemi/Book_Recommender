Book Recommender Chatbot build using the OpenAI API and ChromaDB vectore database to store embedded book titles and summaries. The project uses the OpenAI embedder model to generate said embeddings. On the client side, the project uses a simple front-end build using the streamlit Python library. A /chat endpoint is made available using FastAPI

**Before running, use:**

pip install requirements.txt


**To run the server:**

uvicorn main:app


**To run the client:**

streamlit run homepage.py
