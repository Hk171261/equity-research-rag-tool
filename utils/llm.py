import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
# from langchain_community.chains import RetrievalQAWithSourcesChain
# from langchain_classic.chains import RetrievalQAWithSourcesChain


def answer_query(query, file_path, llm):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FAISS index not found at {file_path}")

    vector_index = FAISS.load_local(
        file_path,
        embeddings=OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    )

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vector_index.as_retriever()
    )

    result = chain({"question": query}, return_only_outputs=True)
    return result