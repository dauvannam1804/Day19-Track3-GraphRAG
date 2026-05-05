import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TRIPLES_FILE = "data/triples.json"
QUESTIONS_FILE = "data/questions.json"

def generate_questions():
    print("--- Đang tạo tập câu hỏi ĐA BƯỚC (Multi-hop) ---")
    
    with open(TRIPLES_FILE, 'r', encoding='utf-8') as f:
        triples = json.load(f)
    
    # Lấy 200 triples để LLM tìm thấy các mối quan hệ liên kết
    sample_triples = triples[:200] 
    triples_str = "\n".join([f"({s}, {p}, {o})" for s, p, o in sample_triples])

    prompt = f"""
    Dựa trên các bộ ba tri thức (triples) dưới đây, hãy tạo ra 10 câu hỏi ĐA BƯỚC (Multi-hop).
    
    Yêu cầu:
    1. Một câu hỏi phải yêu cầu kết nối ít nhất 2-3 mối quan hệ. 
       VD: Thay vì hỏi 'A làm gì?', hãy hỏi 'Công ty đã mua lại A đang đặt trụ sở tại đâu?'
    2. Chỉ hỏi những gì CÓ THỂ trả lời được dựa trên các triples cung cấp.
    3. Định dạng JSON: {{"data": [{{"question": "...", "ground_truth": "..."}}, ...]}}
    
    Dữ liệu Triples:
    {triples_str}
    """

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )

    data = json.loads(response.choices[0].message.content)["data"]
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"--- Đã tạo xong 15 câu hỏi Multi-hop và lưu tại {QUESTIONS_FILE} ---")

if __name__ == "__main__":
    generate_questions()
