Book Recommender Chatbot build using the OpenAI API and ChromaDB vectore database to store embedded book titles and summaries. The project uses the OpenAI embedder model to generate said embeddings. On the client side, the project uses a simple front-end build using the streamlit Python library. A /chat endpoint is made available using FastAPI

**Before running, use:**

pip install requirements.txt

**!!IMPORTANT!!**

BEFORE RUNNING THE SERVER MAKE SURE TO RUN **python3 setup.py**. This creates the embeddings and stores these for the sample books.txt data. Without running this beforehand, the book recommender will NOT work! 


**To run the server:**

uvicorn main:app


**To run the client:**

streamlit run homepage.py
