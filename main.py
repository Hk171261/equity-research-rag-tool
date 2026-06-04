# import streamlit as st
# from langchain_openai import OpenAI
# from utils.fetch import fetch_data_from_urls
# from utils.split import split_documents
# from utils.embeddings import build_and_save_embeddings
# from utils.llm import answer_query
# from dotenv import load_dotenv
#
# load_dotenv()
#
# st.title("Equity Research Tool 📈")
# st.sidebar.title("News Article URLs")
#
# urls = []
# for i in range(2):
#     url = st.sidebar.text_input(f"URL {i+1}")
#     urls.append(url)
#
# process_url_clicked = st.sidebar.button("Process URLs")
# file_path = "vector_index_001"
#
# main_placeholder = st.empty()
# llm = OpenAI(temperature=0.9, max_tokens=500)
#
# if process_url_clicked:
#     main_placeholder.text("Data Loading...Started...✅✅✅")
#     data = fetch_data_from_urls(urls)
#
#     main_placeholder.text("Data Splitting...Started...✅✅✅")
#     docs = split_documents(data, chunk_size=1000)
#
#     main_placeholder.text("Embedding Vector Started Building...✅✅✅")
#     vectorindex_openai = build_and_save_embeddings(docs, file_path)
#     vectorindex_openai.save_local(file_path)
#
# query = main_placeholder.text_input("Question: ")
#
# if query:
#     result = answer_query(query, file_path, llm)
#     st.header("Answer")
#     st.subheader(result["answer"])
#
#     sources = result.get("sources", "")
#     if sources:
#         st.subheader("Sources:")
#         for source in sources.split("\n"):
#             st.write(source)

import streamlit as st
from langchain_openai import OpenAI
from utils.fetch import fetch_data_from_urls
from utils.split import split_documents
from utils.embeddings import build_and_save_embeddings
from utils.llm import answer_query
from dotenv import load_dotenv

load_dotenv()

# ---- Page Config ----
st.set_page_config(page_title="Equity Research Tool", page_icon="📈", layout="centered")


# st.markdown("""
#     <style>
#     * { font-size: 20px !important; }
#     .stTextInput input { font-size: 20px !important; padding: 15px !important; }
#     h1 { font-size: 38px !important; }
#     </style>
# """, unsafe_allow_html=True)

# ---- Title ----
st.title("Equity Research Tool 📈")
# st.markdown(
#     "<h1 style='font-size: 60px;'>Equity Research Tool 📈</h1>",
#     unsafe_allow_html=True
# )

# ---- Session State Init ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "urls_processed" not in st.session_state:
    st.session_state.urls_processed = False

# ---- Sidebar ----
st.sidebar.title("News Article URLs")

urls = []
for i in range(2):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

# ---- Clear/Reset Button ----
if st.sidebar.button("Clear / Reset 🔄"):
    st.session_state.messages = []
    st.session_state.urls_processed = False
    st.rerun()

file_path = "vector_index_001"
llm = OpenAI(temperature=0.9, max_tokens=500)

# ---- Process URLs ----
if process_url_clicked:
    with st.spinner("Fetching articles..."):
        data = fetch_data_from_urls(urls)

    with st.spinner("Splitting documents..."):
        docs = split_documents(data, chunk_size=1000)

    with st.spinner("Building embeddings..."):
        vectorindex_openai = build_and_save_embeddings(docs, file_path)
        vectorindex_openai.save_local(file_path)

    with st.spinner("Generating summary..."):
        summary_result = answer_query(
            "Summarize the key points of these articles in 5 bullet points",
            file_path,
            llm
        )
        st.session_state.summary = summary_result.get("answer", "")

    st.session_state.urls_processed = True
    st.sidebar.success("URLs processed successfully! ✅")

# ---- Chat History ----
if "summary" in st.session_state and st.session_state.summary:
    with st.expander("📰 Article Summary", expanded=True):
        st.write(st.session_state.summary)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("Sources"):
                for source in message["sources"].split("\n"):
                    st.write(source)
        if "confidence" in message:
            st.caption(message["confidence"])

# ---- Chat Input ----
query = st.chat_input("Ask a question about the articles...")

if query:
    if not st.session_state.urls_processed:
        st.warning("Please process URLs first using the sidebar! ⚠️")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = answer_query(query, file_path, llm)
                answer = result.get("answer", "")
                sources = result.get("sources", "")

                # Confidence indicator
                if sources:
                    confidence = "🟢 High Confidence — Answer is sourced"
                else:
                    confidence = "🔴 Low Confidence — No sources found"

                st.write(answer)
                if sources:
                    with st.expander("Sources"):
                        for source in sources.split("\n"):
                            st.write(source)
                st.caption(confidence)

        # Save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "confidence": confidence
        })