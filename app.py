from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import streamlit as st
from utils.fetch import fetch_data_from_urls
from utils.split import split_documents
from utils.embeddings import build_and_save_embeddings
from utils.llm import answer_query
from langchain import OpenAI

import streamlit as st
import requests

st.title("Document QA App")
main_placeholder = st.empty()

# Input URLs
urls_input = st.text_area("Enter URLs (one per line):")
process_url_clicked = st.button("Process URLs")

if process_url_clicked and urls_input.strip():
    urls = urls_input.strip().splitlines()
    main_placeholder.text("Sending URLs to backend...")

    response = requests.post("http://localhost:8000/process-urls", json={"urls": urls})
    if response.status_code == 200:
        main_placeholder.success("✅ Embeddings built successfully!")
    else:
        st.error("Failed to process URLs.")

# Ask a question
query = st.text_input("Ask a question abo"
                      "ut the documents:")

if query:
    response = requests.post("http://localhost:8000/answer", json={"query": query})
    if response.status_code == 200:
        result = response.json()
        st.header("Answer")
        st.subheader(result.get("answer", "No answer found."))

        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            for source in sources.split("\n"):
                st.write(source)
    else:
        st.error("Failed to get answer from backend.")

# app = FastAPI(title="Equity Research Tool")
#
# class ResearchRequest(BaseModel):
#     article_01_url: str
#     article_02_url: str
#
# class ResearchResponse(BaseModel):
#     answer: str
#     sources: str
#
# @app.post("/vector_index", response_model=ResearchResponse)
# def analyze_article(request: ResearchRequest):
#     urls = [request.article_01_url, request.article_02_url]
#     file_path = "vector_index"
#
#     # Data processing
#     data = fetch_data_from_urls(urls)
#     docs = split_documents(data, chunk_size=1000)
#     build_and_save_embeddings(docs, file_path)
#
#     # Answer query (example static query for API)
#     llm = OpenAI(temperature=0.9, max_tokens=500)
#     result = answer_query("What is this article about?", file_path, llm)
#
#     return ResearchResponse(answer=result["answer"], sources=result.get("sources", ""))
# ------------------------------------------------------------------------------------------------
# app = FastAPI(title="Equity Research Tool")
#
# from dotenv import load_dotenv
# load_dotenv()
#
# st.title("Equity Research Tool")
#
# st.sidebar.title("News Article URLs")
#
# urls = []
# for i in range(2):
#     url = st.sidebar.text_input(f"URL {i+1}")
#     urls.append(url)
#
# process_url_clicked = st.sidebar.button("Process URLs")
#
#
# ## Input format
# class ResearchRequest(BaseModel):
#     article_01_url: str
#     article_02_url: str
#
# class ResearchResponse(BaseModel):
#     answer: str
#
# # @app.post("CB Proj 03-Equity Research Tool/vector_index", response_model=ResearchResponse)
# @app.post("/vector_index", response_model=ResearchResponse)
# def analyze_article(urls, file_path):
#     # main_placeholder = st.empty()
#
#     # 1️⃣ Data Loading
#     main_placeholder.text("Data Loading...Started...✅✅✅")
#     data = fetch_data_from_urls(urls)
#
#     # 2️⃣ Data Splitting
#     main_placeholder.text("Data Splitting...Started...✅✅✅")
#     docs = split_documents(data, chunk_size=1000)
#
#     # 3️⃣ Build & Save Embeddings
#     main_placeholder.text("Embedding Vector Started Building...✅✅✅")
#     vector_index = build_and_save_embeddings(docs, file_path)
#
#     # 4️⃣ Question-Answering
#     query = main_placeholder.text_input("Question: ")
#     if query:
#         llm = OpenAI(temperature=0.9, max_tokens=500)
#         result = answer_query(query, file_path, llm)
#
#         st.header("Answer")
#         st.subheader(result["answer"])
#
#         sources = result.get("sources", "")
#         if sources:
#             st.subheader("Sources:")
#             for source in sources.split("\n"):
#                 st.write(source)


    # return ResearchResponse(answer=f"Analysis for {data.company} from {data.article_url}")
