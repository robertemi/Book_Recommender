import streamlit as st
import requests

API_URL = 'http://localhost:8000/chat'

st.set_page_config(page_title="Book Recommender", page_icon="📚")
st.title("📚 Book Recommender")


user_q = st.chat_input("What would you like to read?")

if user_q:
    with st.spinner("Processing..."):
        try:
            resp = requests.post(API_URL, json={"user_prompt": user_q}, timeout=30)
            if resp.status_code == 200:
                reply = resp.json()["chat_response"]
                st.markdown(reply)
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")