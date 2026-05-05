import json
import pandas as pd
import os
import sys
from flat_rag import query_flat_rag
from graph_rag import query_graph_rag
from openai import OpenAI
from dotenv import load_dotenv

# Class để vừa in ra màn hình vừa ghi vào file log
class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass

# Class để chặn các print từ các module khác
class SuppressPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

QUESTIONS_FILE = "data/questions.json"
REPORT_FILE = "reports/benchmark_report.md"
LOG_FILE = "reports/benchmark_console.log"

def evaluate_answer(question, answer, ground_truth):
    prompt = f"""
    Hãy chấm điểm câu trả lời sau đây dựa trên Đáp án chuẩn (Ground Truth).
    
    Câu hỏi: {question}
    Đáp án chuẩn: {ground_truth}
    Câu trả lời cần chấm: {answer}
    
    Trả về JSON: {{"score": X, "reason": "..."}} (Thang điểm 10)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except:
        return {"score": 0, "reason": "Lỗi đánh giá"}

def run_benchmark():
    os.makedirs("reports", exist_ok=True)
    sys.stdout = Logger(LOG_FILE)

    if not os.path.exists(QUESTIONS_FILE):
        print("Lỗi: Chạy src/generate_questions.py trước!")
        return

    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Chỉ lấy 10 câu đầu tiên theo yêu cầu
    data = data[:10]

    results = []
    print("\n" + "="*60)
    print("🚀 BẮT ĐẦU CHẠY BENCHMARK: FLAT RAG VS GRAPHRAG (NÂNG CẤP)")
    print("="*60)
    
    for i, item in enumerate(data):
        q = item['question']
        gt = item['ground_truth']
        
        print(f"\n🔍 [Câu hỏi {i+1}/{len(data)}]: {q}")
        print(f"🎯 [Ground Truth]: {gt}")
        
        # --- FLAT RAG ---
        with SuppressPrint():
            flat_ans, flat_ctx = query_flat_rag(q)
        flat_eval = evaluate_answer(q, flat_ans, gt)
        print(f"📦 [Flat RAG Context]:\n{flat_ctx}")
        print(f"📄 [Flat RAG Ans]: {flat_ans}")
        print(f"⭐ Điểm: {flat_eval['score']}/10")
        
        # --- GRAPHRAG ---
        try:
            with SuppressPrint():
                graph_ans, graph_ctx = query_graph_rag(q)
            graph_eval = evaluate_answer(q, graph_ans, gt)
            print(f"🕸️ [GraphRAG Context]:\n{graph_ctx}")
            print(f"📄 [GraphRAG Ans]: {graph_ans}")
            print(f"⭐ Điểm: {graph_eval['score']}/10")
        except Exception as e:
            print(f"❌ [GraphRAG Lỗi]: {e}")
            graph_ans, graph_ctx, graph_eval = "Error", "", {"score": 0}
        
        print("-" * 40)
        results.append({
            "Question": q, "Ground Truth": gt,
            "Flat RAG": flat_ans, "Flat Context": flat_ctx, "Flat Score": flat_eval['score'],
            "GraphRAG": graph_ans, "Graph Context": graph_ctx, "Graph Score": graph_eval['score']
        })

    # Báo cáo MD
    df = pd.DataFrame(results)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Benchmark Report (Detailed)\n\n")
        f.write(f"- Avg Flat RAG: {df['Flat Score'].mean():.2f}\n")
        f.write(f"- Avg GraphRAG: {df['Graph Score'].mean():.2f}\n\n")
        for i, res in enumerate(results):
            f.write(f"### {i+1}. {res['Question']}\n")
            f.write(f"**GT:** {res['Ground Truth']}\n")
            f.write(f"**Flat Context:** {res['Flat Context'][:300]}...\n")
            f.write(f"**Graph Context:**\n{res['Graph Context'][:300]}...\n")
            f.write(f"**Flat RAG ({res['Flat Score']}):** {res['Flat RAG']}\n")
            f.write(f"**GraphRAG ({res['Graph Score']}):** {res['GraphRAG']}\n\n")

    print(f"\n✅ HOÀN THÀNH! Log: {LOG_FILE}")

if __name__ == "__main__":
    run_benchmark()
