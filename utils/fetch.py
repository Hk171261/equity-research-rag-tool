# from langchain_community.document_loaders import UnstructuredURLLoader
#
# def fetch_data_from_urls(urls: list):
#     loader = UnstructuredURLLoader(urls=urls)
#     data = loader.load()
#     return data

from langchain_community.document_loaders import NewsURLLoader

def fetch_data_from_urls(urls: list):
    loader = NewsURLLoader(urls=urls)
    data = loader.load()
    for doc in data:
        if "source" not in doc.metadata:
            doc.metadata["source"] = "unknown"
    return data