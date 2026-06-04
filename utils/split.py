from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(data, chunk_size=1000):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=chunk_size
    )
    docs = text_splitter.split_documents(data)
    return docs