from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from utils.fetch import fetch_data_from_urls
from utils.split import split_documents
from utils.embeddings import build_and_save_embeddings
from utils.llm import answer_query

app = FastAPI()
VECTOR_INDEX_PATH = "my_index"


# Request models
class URLRequest(BaseModel):
    urls: List[str]


class QueryRequest(BaseModel):
    query: str


@app.post("/process-urls")
def process_urls(request: URLRequest):
    print("🔧 Received /process-urls request")
    print(f"📥 URLs: {request.urls}")

    try:
        data = fetch_data_from_urls(request.urls)
        print(f"✅ Fetched data: {len(data)} characters")
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return {"status": "error", "message": f"Error fetching data: {e}"}

    try:
        docs = split_documents(data, chunk_size=1000)
        print(f"✅ Split into {len(docs)} documents")
    except Exception as e:
        print(f"❌ Error splitting documents: {e}")
        return {"status": "error", "message": f"Error splitting documents: {e}"}

    try:
        vector_index = build_and_save_embeddings(docs, VECTOR_INDEX_PATH)
        print("✅ Built embeddings")
    except Exception as e:
        print(f"❌ Error building embeddings: {e}")
        return {"status": "error", "message": f"Error building embeddings: {e}"}

    try:
        vector_index.save_local(VECTOR_INDEX_PATH)
        print(f"💾 Saved vector index to: {VECTOR_INDEX_PATH}")
    except Exception as e:
        print(f"❌ Error saving vector index: {e}")
        return {"status": "error", "message": f"Error saving index: {e}"}

    return {"status": "success", "message": "Embeddings built and saved"}


@app.post("/answer")
def answer(request: QueryRequest):
    print("🤖 Received /answer request")
    print(f"📥 Query: {request.query}")

    try:
        result = answer_query(request.query, VECTOR_INDEX_PATH, llm="openai")
        print(f"✅ Answer generated: {result.get('answer')}")
        return result
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        return {"status": "error", "message": f"Error answeringquery:{e}"}