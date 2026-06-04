from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def build_and_save_embeddings(docs, file_path):
    embeddings = OpenAIEmbeddings()
    vector_index = FAISS.from_documents(docs, embeddings)
    vector_index.save_local(file_path)
    return vector_index