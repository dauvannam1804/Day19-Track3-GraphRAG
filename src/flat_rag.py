import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Cấu hình
CHROMA_PATH = "data/chroma_db"
INPUT_FILE = "data/filtered_corpus.csv"

# Khởi tạo sẵn để tăng tốc
_embeddings = None
_vectorstore = None

def get_vectorstore():
    global _embeddings, _vectorstore
    if _vectorstore is None:
        _embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        _vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=_embeddings)
    return _vectorstore

def build_flat_rag():
    print("--- Đang khởi tạo Flat RAG (ChromaDB) ---")
    df = pd.read_csv(INPUT_FILE)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = []
    for _, row in df.iterrows():
        chunks = text_splitter.split_text(row['text'])
        for chunk in chunks:
            docs.append({"content": chunk, "metadata": {"title": row['title']}})
    
    texts = [d["content"] for d in docs]
    metadatas = [d["metadata"] for d in docs]
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    if os.path.exists(CHROMA_PATH):
        import shutil
        shutil.rmtree(CHROMA_PATH)
    vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas, persist_directory=CHROMA_PATH)
    print(f"--- Đã hoàn thành indexing {len(docs)} chunks ---")
    return vectorstore

def query_flat_rag(question):
    vectorstore = get_vectorstore()
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    
    # Tìm kiếm context
    docs = vectorstore.similarity_search(question, k=3)
    context_text = "\n---\n".join([d.page_content for d in docs])
    
    system_prompt = (
        "You are an assistant for question-answering tasks. Use the context to answer.\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
    
    chain = prompt | llm
    response = chain.invoke({"context": context_text, "input": question})
    
    return response.content, context_text

if __name__ == "__main__":
    if not os.path.exists(CHROMA_PATH):
        build_flat_rag()
    ans, ctx = query_flat_rag("Who founded OpenAI?")
    print(f"Ans: {ans}")
