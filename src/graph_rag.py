import os
import json
import re
import time
from dotenv import load_dotenv
from neo4j import GraphDatabase, READ_ACCESS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Cấu hình Neo4j
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def get_graph_context(entities):
    if not entities:
        return ""
        
    context_triples = set()
    
    # Chuẩn hóa từ khóa
    search_keywords = []
    for ent in entities:
        words = re.findall(r'\w+', ent)
        search_keywords.extend([w for w in words if len(w) > 3])

    # Cơ chế Retry để tránh lỗi Routing
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as driver:
                with driver.session(default_access_mode=READ_ACCESS) as session:
                    for kw in search_keywords:
                        # Truy vấn 2-hop để hỗ trợ câu hỏi phức tạp
                        query = (
                            "MATCH (e:Entity)-[r1]->(n1) "
                            "WHERE toLower(e.name) CONTAINS toLower($kw) "
                            "OR toLower(replace(e.name, '_', ' ')) CONTAINS toLower($kw) "
                            "OPTIONAL MATCH (n1)-[r2]->(n2) "
                            "RETURN e.name as s1, type(r1) as p1, n1.name as o1, "
                            "type(r2) as p2, n2.name as o2 "
                            "LIMIT 50"
                        )
                        result = session.run(query, kw=kw)
                        for record in result:
                            context_triples.add(f"({record['s1']})--[{record['p1']}]-->({record['o1']})")
                            if record['p2']:
                                context_triples.add(f"({record['o1']})--[{record['p2']}]-->({record['o2']})")
            break # Thành công thì thoát vòng lặp retry
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Lỗi kết nối (Lần {attempt+1}), đang thử lại...")
                time.sleep(2)
            else:
                return f"ERROR_CONNECTION: {str(e)}"
                
    return "\n".join(list(context_triples))

def query_graph_rag(question):
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    
    # Bước 1: Trích xuất thực thể
    ner_prompt = ChatPromptTemplate.from_template("Extract main entities from: {question}. Return comma separated.")
    ner_chain = ner_prompt | llm
    ner_output = ner_chain.invoke({"question": question}).content
    entities = [e.strip() for e in ner_output.split(",")]
    
    # Bước 2: Lấy tri thức từ đồ thị
    graph_context = get_graph_context(entities)
    
    # Bước 3: Trả lời
    system_prompt = (
        "You are a GraphRAG assistant. Use the Knowledge Graph context below.\n"
        "If you can't find the answer in the context, say you don't know.\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
    
    rag_chain = prompt | llm
    response = rag_chain.invoke({"context": graph_context, "input": question})
    return response.content, graph_context

if __name__ == "__main__":
    ans, ctx = query_graph_rag("Who is Ada Lovelace?")
    print(ans)
