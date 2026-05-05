# GraphRAG vs Flat RAG Benchmark Pipeline

Dự án này triển khai một Pipeline so sánh hiệu năng giữa hai phương pháp truy vấn tri thức: **Flat RAG (Vector Search)** và **GraphRAG (Knowledge Graph)**. Mục tiêu là chứng minh sức mạnh của đồ thị tri thức trong việc giải quyết các câu hỏi đa bước (Multi-hop).

## 🚀 Quy trình thực hiện (Workflow)

Hệ thống bao gồm 4 giai đoạn chính:

1. **Giai đoạn 1: Chuẩn bị dữ liệu (`prepare_data.py`)**
   - Lọc dữ liệu từ bộ Corpus gốc.
   - Chỉ lấy 50 bài báo chất lượng nhất liên quan đến các công ty AI và Công nghệ.
   - Kết quả: Lưu tại `data/filtered_corpus.json`.

2. **Giai đoạn 2: Xây dựng Đồ thị tri thức (`indexing.py`)**
   - Sử dụng LLM để trích xuất thực thể (Entities) và các mối quan hệ (Triples).
   - Đẩy dữ liệu lên **Neo4j Aura**.
   - Khởi tạo ChromaDB cho Flat RAG.

3. **Giai đoạn 3: Tạo câu hỏi thử nghiệm (`generate_questions.py`)**
   - Phân tích các bộ ba (Triples) trong đồ thị.
   - LLM tự động tạo 10 câu hỏi đa bước (Multi-hop) có độ khó cao.
   - Kết quả: Lưu tại `data/questions.json`.

4. **Giai đoạn 4: Đánh giá & So sánh (`benchmark.py`)**
   - Chạy đối đầu Flat RAG vs GraphRAG.
   - Sử dụng LLM làm trọng tài (LLM-as-a-judge) để chấm điểm từ 0-10.
   - Kết quả: Xuất báo cáo chi tiết tại `reports/benchmark_report.md` và log tại `reports/benchmark_console.log`.

---

## 🛠 Hướng dẫn cài đặt (Setup)

### 1. Yêu cầu hệ thống
- Python 3.10+
- Công cụ quản lý thư viện `uv` (Khuyến nghị).

### 2. Cài đặt Dependencies
```bash
# Cài đặt các thư viện cần thiết
uv pip install -r pyproject.toml
```

### 3. Cấu hình biến môi trường
Tạo file `.env` tại thư mục gốc với các thông tin sau:
```env
OPENAI_API_KEY=your_openai_api_key
NEO4J_URI=neo4j+s://your_neo4j_instance
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

---

## 🏃‍♂️ Cách chạy (Execution)

Bạn có thể chạy từng bước theo thứ tự sau:

```bash
# 1. Lọc dữ liệu
uv run python3 src/prepare_data.py

# 2. Trích xuất và Indexing lên Neo4j/ChromaDB
uv run python3 src/indexing.py

# 3. Tạo tập câu hỏi Benchmark
uv run python3 src/generate_questions.py

# 4. Chạy Benchmark so sánh
uv run python3 src/benchmark.py
```

---

## 📊 Kết quả đầu ra
Sau khi chạy xong, bạn sẽ nhận được:
- **`reports/final_report.md`**: Bản báo cáo phân tích chuyên sâu về ưu/nhược điểm của từng phương pháp.
- **`reports/benchmark_console.log`**: Toàn bộ quá trình truy vấn và ngữ cảnh (Context) mà hệ thống đã lấy ra.
