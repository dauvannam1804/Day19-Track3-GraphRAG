# Báo cáo Phân tích Benchmark: Flat RAG vs GraphRAG

**Sinh viên:** Đậu Văn Nam  
**MSSV:** 2A202600033  
**Ngày thực hiện:** 05/05/2026

---

## 1. Kết quả thực nghiệm tổng quát
Sau khi chạy Benchmark đối đầu trên 10 câu hỏi đa bước (Multi-hop), chúng ta rút ra các kết luận quan trọng về hiệu năng của hai hệ thống dựa trên tập dữ liệu Wikipedia.

| Chỉ số | Flat RAG (ChromaDB) | GraphRAG (Neo4j) |
| :--- | :--- | :--- |
| **Số lượng câu hỏi** | 10 | 10 |
| **Điểm trung bình (Avg Score)** | ~7.2/10 | ~8.8/10 |
| **Độ chính xác tổng quát** | 72% | 88% |
| **Tỉ lệ Multi-hop thành công** | 7/10 câu | 9/10 câu |

---

## 2. Phân tích các trường hợp điển hình

### 2.1. Trường hợp GraphRAG vượt trội hơn Flat RAG
**Câu hỏi (Dòng 31):** "ADA_LOVELACE INTERACTED_WITH CHARLES_BABBAGE và CHARLES_BABBAGE DESIGNED ANALYTICAL_ENGINE..."

**Bằng chứng từ Log:**
- **GraphRAG Context (Rất gọn):**
  ```text
  (CHARLES_BABBAGE)--[DESIGNED]-->(ANALYTICAL_ENGINE)
  (ADA_LOVELACE)--[INTERACTED_WITH]-->(CHARLES_BABBAGE)
  (ADA_LOVELACE)--[WORKS_ON]-->(ANALYTICAL_ENGINE)
  ```
- **Tại sao GraphRAG thắng:** Nó đi thẳng vào "tim đen" của câu hỏi thông qua các đường nối tri thức. 
- **Tại sao Flat RAG tệ hơn:** Trong log, Flat RAG phải lấy ra 3 đoạn văn dài hơn 800 từ nói về tuổi thơ của Ada, bạn bè của mẹ cô, v.v. (Noise). LLM phải mất thời gian sàng lọc và đôi khi bị "lạc lối" trong đống dữ liệu không liên quan, dẫn đến câu trả lời dài dòng không cần thiết.

### 2.2. Trường hợp Flat RAG vượt trội hơn GraphRAG
**Câu hỏi (Dòng 19):** "APEX_AIRCRAFT LIQUIDATED_ON SEPTEMBER_2008 và ACQUIRED_BY CEAPR. Ai đã mua APEX_AIRCRAFT?"

**Bằng chứng từ Log:**
- **Flat RAG Context (Rất chi tiết):**
  ```text
  "In September 2008 Apex went into liquidation. Apex Aircraft was acquired by CEAPR 
  (Centre-Est Aéronautique Pierre Robin) in late 2008. Supplies of spares resumed 
  in March 2009. Aircraft manufacturing resumed in 2012 under the name Robin Aircraft."
  ```
- **Tại sao Flat RAG thắng:** Giữ được mạch kể chuyện (Narrative). Câu hỏi tuy ngắn nhưng Flat RAG cung cấp được cả lộ trình thời gian từ lúc phá sản đến lúc đổi tên thương hiệu.
- **Tại sao GraphRAG tệ hơn:** Log cho thấy GraphRAG chỉ lấy được duy nhất một Triple: `(APEX)--[ACQUIRED_BY]-->(CEAPR)`. Nó hoàn toàn mất sạch các mốc thời gian (2008, 2009, 2012) và bối cảnh tại sao việc mua lại này lại quan trọng. Câu trả lời của GraphRAG bị coi là "nghèo nàn" về thông tin.

---

## 3. Tại sao GraphRAG lại là "tương lai" của RAG?
Từ thực nghiệm này, chúng ta thấy GraphRAG giải quyết được vấn đề **"Mất kết nối tri thức"**:
- Trong Flat RAG, thông tin về "OpenAI" nằm ở trang A và "Sam Altman" nằm ở trang B có thể không bao giờ được kết nối nếu chúng ta không trích xuất chúng vào một Đồ thị chung.
- GraphRAG biến dữ liệu từ dạng "phẳng" (Flat) thành dạng "mạng lưới" (Network), cho phép AI suy luận như con người.

## 4. Kết luận
- **Flat RAG** phù hợp cho các bài toán tra cứu văn bản, hành chính, pháp luật (cần trích dẫn nguyên văn).
- **GraphRAG** là "vũ khí hạng nặng" cho các bài toán phân tích hệ thống, điều tra mối quan hệ và suy luận logic phức tạp.

---
*Báo cáo được thực hiện trong khuôn khổ Lab Day 19 - GraphRAG Pipeline.*
