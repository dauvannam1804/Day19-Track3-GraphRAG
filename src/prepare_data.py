import pandas as pd
import os

# Đường dẫn file
INPUT_FILE = "data/train-00000-of-00001.parquet"
OUTPUT_FILE = "data/filtered_corpus.csv"

# Danh sách các công ty và từ khóa liên quan đến AI để lọc
AI_COMPANIES = [
    "OpenAI", "Anthropic", "DeepMind", "Google DeepMind", "Microsoft AI", 
    "Meta AI", "NVIDIA", "Mistral AI", "Cohere", "Stability AI", 
    "Hugging Face", "X.AI", "Grok", "Midjourney", "Perplexity AI", 
    "Sam Altman", "Demis Hassabis", "Ilya Sutskever", "Jensen Huang"
]

def prepare_data():
    print(f"--- Đang đọc dữ liệu từ {INPUT_FILE} ---")
    if not os.path.exists(INPUT_FILE):
        print(f"Lỗi: Không tìm thấy file {INPUT_FILE}")
        return

    # Đọc file parquet
    df = pd.read_parquet(INPUT_FILE)
    print(f"Tổng số bản ghi ban đầu: {len(df)}")

    # Lọc theo Title (khớp chính xác hoặc chứa tên công ty)
    # Chúng ta dùng regex để tìm kiếm không phân biệt chữ hoa chữ thường
    pattern = '|'.join(AI_COMPANIES)
    
    print(f"--- Đang lọc dữ liệu với các từ khóa: {AI_COMPANIES} ---")
    
    # Ưu tiên 1: Lọc theo Title
    df_filtered = df[df['title'].str.contains(pattern, case=False, na=False)]
    
    # Nếu chưa đủ 50 bài, mở rộng lọc theo nội dung (text)
    if len(df_filtered) < 50:
        print(f"Chỉ tìm thấy {len(df_filtered)} bài qua Title. Đang mở rộng tìm kiếm trong nội dung...")
        df_remaining = df[~df.index.isin(df_filtered.index)]
        df_text_match = df_remaining[df_remaining['text'].str.contains(pattern, case=False, na=False)]
        
        # Lấy thêm để đủ 50 hoặc tối đa có thể
        needed = 50 - len(df_filtered)
        df_filtered = pd.concat([df_filtered, df_text_match.head(needed)])

    print(f"Số lượng bản ghi sau khi lọc: {len(df_filtered)}")

    # Lưu kết quả
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_filtered.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"--- Đã lưu dữ liệu lọc được vào {OUTPUT_FILE} ---")

if __name__ == "__main__":
    prepare_data()
