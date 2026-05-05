import pandas as pd
import json
import os
from openai import OpenAI
from neo4j import GraphDatabase
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Cấu hình OpenAI & Neo4j
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Đường dẫn file
INPUT_FILE = "data/filtered_corpus.csv"
TRIPLES_FILE = "data/triples.json"

# Bảng giá ước tính cho gpt-5-nano
PRICE_INPUT = 0.050 / 1_000_000
PRICE_OUTPUT = 0.200 / 1_000_000

def extract_triples_from_text(text, title):
    """Sử dụng LLM để trích xuất thực thể và quan hệ."""
    prompt = f"""
    Bạn là một chuyên gia về xây dựng Đồ thị tri thức (Knowledge Graph).
    Nhiệm vụ của bạn là đọc đoạn văn bản về công ty công nghệ sau đây và trích xuất các bộ ba (triples) dưới dạng: (Subject, Predicate, Object).
    
    Yêu cầu:
    1. Chỉ trích xuất các thực thể quan trọng như: Người, Công ty, Công nghệ, Sự kiện, Năm thành lập, Vị trí chức vụ.
    2. Quan hệ (Predicate) nên súc tích, viết hoa và dùng dấu gạch dưới (VD: FOUNDED_BY, WORKS_AT, COMPETES_WITH).
    3. Trả về kết quả dưới định dạng JSON duy nhất như sau: {{"triples": [["Subject", "Predicate", "Object"], ...]}}
    4. Nếu không có thông tin, trả về {{"triples": []}}.
    
    Văn bản nguồn (Tiêu đề: {title}):
    {text[:2000]}  # Giới hạn 2000 ký tự để tiết kiệm token
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "system", "content": "You are a helpful assistant that extracts structured data."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        content = json.loads(response.choices[0].message.content)
        triples = content.get("triples", content.get("data", [])) # Xử lý linh hoạt key trả về
        
        usage = response.usage
        cost = (usage.prompt_tokens * PRICE_INPUT) + (usage.completion_tokens * PRICE_OUTPUT)
        
        return triples, usage.total_tokens, cost
    except Exception as e:
        print(f"Lỗi khi gọi OpenAI cho bài '{title}': {e}")
        return [], 0, 0

def push_to_neo4j(triples):
    """Đẩy các bộ ba vào Neo4j."""
    if not triples:
        return
        
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        for s, p, o in triples:
            # Câu lệnh Cypher để tạo Node và Relationship (dùng MERGE để tránh trùng lặp)
            query = (
                "MERGE (a:Entity {name: $sub}) "
                "MERGE (b:Entity {name: $obj}) "
                f"MERGE (a)-[r:{p}]->(b)"
            )
            session.run(query, sub=str(s), obj=str(o))
    driver.close()

def main():
    print("--- Bắt đầu quy trình Indexing (NER & Neo4j) ---")
    df = pd.read_csv(INPUT_FILE)
    
    all_triples = []
    total_tokens = 0
    total_cost = 0
    
    # Để an toàn, chúng ta xử lý từng bài một
    for index, row in df.iterrows():
        print(f"[{index+1}/{len(df)}] Đang xử lý: {row['title']}...")
        
        triples, tokens, cost = extract_triples_from_text(row['text'], row['title'])
        
        if triples:
            # Lưu vào danh sách tổng
            all_triples.extend(triples)
            # Đẩy lên Neo4j ngay lập tức
            push_to_neo4j(triples)
            print(f"   -> Trích xuất được {len(triples)} triples. Cost: ${cost:.5f}")
        
        total_tokens += tokens
        total_cost += cost
        
        # Nghỉ một chút để tránh Rate Limit nếu cần
        time.sleep(0.5)

    # Lưu toàn bộ triples vào file cục bộ
    with open(TRIPLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_triples, f, ensure_ascii=False, indent=4)
        
    print("\n--- HOÀN THÀNH ---")
    print(f"Tổng số Triples đã lưu và đẩy lên Neo4j: {len(all_triples)}")
    print(f"Tổng Tokens đã dùng: {total_tokens}")
    print(f"Tổng chi phí ước tính: ${total_cost:.4f}")
    print(f"Dữ liệu triples đã được lưu tại: {TRIPLES_FILE}")

if __name__ == "__main__":
    main()
