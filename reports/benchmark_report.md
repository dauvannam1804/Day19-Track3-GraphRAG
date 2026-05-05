# Benchmark Report (Detailed)

- Avg Flat RAG: 8.90
- Avg GraphRAG: 9.00

### 1. APEX_AIRCRAFT MARKETs ROBIN_RANGE và ROBIN_RANGE được FORMERLY_IDENTICAL_TO AVIONS_ROBIN_DR400_4_SEATER. Mô hình AVIONS_ROBIN_DR400_4_SEATER là gì?
**GT:** AVIONS_ROBIN_DR400_4_SEATER
**Flat Context:** Apex Aircraft was a French company devoted to light aeroplane manufacture. It markets three ranges of light aircraft which it brands Robin, Alpha and CAP. The "Robin" range is the former Avions Robin DR400 4-seater aircraft of wooden construction, the "Alpha" range is the former Avions Robin R2000 a...
**Graph Context:**
(APEX_AIRCRAFT)--[MARKETS]-->(ALPHA_RANGE)
(CAP_RANGE)--[FORMERLY_IDENTICAL_TO]-->(MUDRY_CAP_AVIATION_CAP_232)
(ALPHA_RANGE)--[FORMERLY_IDENTICAL_TO]-->(AVIONS_ROBIN_R2000_ALL_METAL_2_SEATER)
(APEX_AIRCRAFT)--[LIQUIDATED_ON]-->(SEPTEMBER_2008)
(CAP_RANGE)--[FORMERLY_IDENTICAL_TO]-->(MUDRY_CAP_AVIATI...
**Flat RAG (10):** AVIONS_ROBIN_DR400_4_SEATER là Avions Robin DR400 4-seater, một máy bay hạng nhẹ 4 chỗ với kết cấu bằng gỗ do hãng Avions Robin (Pháp) chế tạo. Đây là mẫu máy bay tiền thân cho các dòng Robin được Apex Aircraft sau này tiếp thị (Robin/Alpha).
**GraphRAG (10):** AVIONS_ROBIN_DR400_4_SEATER là một mô hình máy bay hạng nhẹ 4 chỗ do Avions Robin sản xuất, thuộc dòng Robin DR400. Nói cách khác, đây là phiên bản 4 chỗ của dòng DR400, và theo đồ thị, ROBIN_RANGE được formerly identical to this model.

### 2. ROBIN_R2000 được TRANSFERRED_TO đến ALPHA_AVIATION_NEW_ZEALAND và ROBIN_R2000_TYPE_CERTIFICATES được TRANSFERRED_TO ALPHA_AVIATION_NEW_ZEALAND. Ai là người nhận cả hai chuyển giao này?
**GT:** ALPHA_AVIATION_NEW_ZEALAND
**Flat Context:** Apex Aircraft was a French company devoted to light aeroplane manufacture. It markets three ranges of light aircraft which it brands Robin, Alpha and CAP. The "Robin" range is the former Avions Robin DR400 4-seater aircraft of wooden construction, the "Alpha" range is the former Avions Robin R2000 a...
**Graph Context:**
...
**Flat RAG (10):** Alpha Aviation ở New Zealand.
**GraphRAG (0):** Xin lỗi, tôi không có thông tin trong ngữ cảnh để xác định người nhận của cả hai chuyển giao. Nếu bạn cung cấp dữ liệu đồ thị hoặc mô tả các giao dịch (ví dụ các nút và quan hệ TRANSFERRED_TO), tôi có thể giúp tìm người nhận chung.

### 3. CAP_RANGE được FORMERLY_IDENTICAL_TO MUDRY_CAP_AVIATION_CAP_10 và CAP_RANGE được FORMERLY_IDENTICAL_TO MUDRY_CAP_AVIATION_CAP_232. Hãy nêu các mô hình được FORMERLY_IDENTICAL_TO CAP_RANGE.
**GT:** MUDRY_CAP_AVIATION_CAP_10; MUDRY_CAP_AVIATION_CAP_232
**Flat Context:** Apex Aircraft was a French company devoted to light aeroplane manufacture. It markets three ranges of light aircraft which it brands Robin, Alpha and CAP. The "Robin" range is the former Avions Robin DR400 4-seater aircraft of wooden construction, the "Alpha" range is the former Avions Robin R2000 a...
**Graph Context:**
...
**Flat RAG (10):** Các mô hình được FORMERLY_IDENTICAL_TO CAP_RANGE là:
- Mudry/CAP Aviation CAP-10
- Mudry/CAP Aviation CAP-232

(Nghĩa là CAP_RANGE từng giống với CAP-10 và CAP-232.)
**GraphRAG (10):** - MUDRY_CAP_AVIATION_CAP_10
- MUDRY_CAP_AVIATION_CAP_232

### 4. ROBIN_R2000 đã được TRANSFERRED_TO ALPHA_AVIATION_NEW_ZEALAND và ROBIN_R2000 được MARKETED_AS ALPHA_2000. Tên được dùng để MARKETING ROBIN_R2000 là gì?
**GT:** ALPHA_2000
**Flat Context:** Apex Aircraft was a French company devoted to light aeroplane manufacture. It markets three ranges of light aircraft which it brands Robin, Alpha and CAP. The "Robin" range is the former Avions Robin DR400 4-seater aircraft of wooden construction, the "Alpha" range is the former Avions Robin R2000 a...
**Graph Context:**
(ROBIN_R2000_TYPE_CERTIFICATES)--[TRANSFERRED_TO]-->(ALPHA_AVIATION_NEW_ZEALAND)
(ROBIN_R2000)--[TRANSFERRED_TO]-->(ALPHA_AVIATION_NEW_ZEALAND)
(ROBIN_R2000)--[MARKETED_AS]-->(ALPHA_2000)...
**Flat RAG (0):** Alpha 2000.
**GraphRAG (10):** ALPHA_2000.

Giải thích: theo đồ thị, ROBIN_R2000 được MARKED_AS (MARKETED_AS) bởi ALPHA_2000.

### 5. APEX_AIRCRAFT LIQUIDATED_ON SEPTEMBER_2008 và ACQUIRED_BY CEAPR. Ai đã mua APEX_AIRCRAFT?
**GT:** CEAPR
**Flat Context:** In September 2008 Apex went into liquidation. Apex Aircraft was acquired by CEAPR (Centre-Est Aéronautique Pierre Robin) in late 2008.  Supplies of spares resumed in March 2009. Aircraft manufacturing resumed in 2012 under the name Robin Aircraft.

Aircraft
Mudry CAP 10
Mudry CAP 20
Mudry CAP 230

R...
**Graph Context:**
(APEX_AIRCRAFT)--[MARKETS]-->(ALPHA_RANGE)
(CAP_RANGE)--[FORMERLY_IDENTICAL_TO]-->(MUDRY_CAP_AVIATION_CAP_232)
(ALPHA_RANGE)--[FORMERLY_IDENTICAL_TO]-->(AVIONS_ROBIN_R2000_ALL_METAL_2_SEATER)
(APEX_AIRCRAFT)--[LIQUIDATED_ON]-->(SEPTEMBER_2008)
(CAP_RANGE)--[FORMERLY_IDENTICAL_TO]-->(MUDRY_CAP_AVIATI...
**Flat RAG (10):** Người mua Apex Aircraft là CEAPR (Centre-Est Aéronautique Pierre Robin), một công ty hàng không của Pháp. CEAPR nhận được Apex vào cuối năm 2008 sau khi Apex bị thanh lý vào tháng 9/2008.
**GraphRAG (10):** CEAPR đã mua APEX_AIRCRAFT.

### 6. APEX_AIRCRAFT ACQUIRED_BY CEAPR và APEX_AIRCRAFT REBRANDED_AS ROBIN_AIRCRAFT. Thương hiệu mới khi được rebranded là gì?
**GT:** ROBIN_AIRCRAFT
**Flat Context:** Apex Aircraft was a French company devoted to light aeroplane manufacture. It markets three ranges of light aircraft which it brands Robin, Alpha and CAP. The "Robin" range is the former Avions Robin DR400 4-seater aircraft of wooden construction, the "Alpha" range is the former Avions Robin R2000 a...
**Graph Context:**
(APEX_AIRCRAFT)--[MARKETS]-->(ALPHA_RANGE)
(CAP_RANGE)--[FORMERLY_IDENTICAL_TO]-->(MUDRY_CAP_AVIATION_CAP_232)
(ALPHA_RANGE)--[FORMERLY_IDENTICAL_TO]-->(AVIONS_ROBIN_R2000_ALL_METAL_2_SEATER)
(APEX_AIRCRAFT)--[LIQUIDATED_ON]-->(SEPTEMBER_2008)
(CAP_RANGE)--[FORMERLY_IDENTICAL_TO]-->(MUDRY_CAP_AVIATI...
**Flat RAG (10):** Robin Aircraft. Sau khi CEAPR mua lại Apex vào cuối 2008, việc sản xuất được tiếp tục vào năm 2012 dưới tên Robin Aircraft.
**GraphRAG (10):** Thương hiệu mới sau khi rebranded là ROBIN_AIRCRAFT (Robin Aircraft).

### 7. NONCOHERENT_SPACE_TIME_CODES PROPOSED_BY TOM_MARZETTA và BERTRAND_HOCHWALD. Ai là những người đã đề xuất NONCOHERENT_SPACE_TIME_CODES?
**GT:** TOM_MARZETTA; BERTRAND_HOCHWALD
**Flat Context:** Non-coherent space time codes are a way of transmitting data in wireless communications. 
In this multiple antenna scheme, it is assumed that the receiver only has knowledge of the statistics of channel.
Non-coherent space-time transmission schemes were proposed by Tom Marzetta and Bertrand Hochwald...
**Graph Context:**
...
**Flat RAG (10):** Tom Marzetta và Bertrand Hochwald. (Vào năm 1999.)
**GraphRAG (10):** Tom Marzetta và Bertrand Hochwald.

### 8. ADA_LOVELACE INTERACTED_WITH CHARLES_BABBAGE và CHARLES_BABBAGE DESIGNED ANALYTICAL_ENGINE. Máy tính nào được thiết kế bởi Charles Babbage mà ADA Lovelace đã tương tác?
**GT:** ANALYTICAL_ENGINE
**Flat Context:** Lovelace first met Charles Babbage in June 1833, through their mutual friend Mary Somerville. Later that month, Babbage invited Lovelace to see the prototype for his difference engine. She became fascinated with the machine and used her relationship with Somerville to visit Babbage as often as she c...
**Graph Context:**
(CHARLES_BABBAGE)--[DESIGNED]-->(ANALYTICAL_ENGINE)
(ADA_LOVELACE)--[INTERACTED_WITH]-->(CHARLES_WHEATSTONE)
(WILLIAM_KING)--[BECAME_TITLE]-->(EARL_OF_LOVELACE)
(ADA_LOVELACE)--[OCCUPATION]-->(MATHEMATICIAN)
(ADA_LOVELACE)--[INTERACTED_WITH]-->(SIR_DAVID_BREWSTER)
(ADA_LOVELACE)--[WORKS_ON]-->(ANALY...
**Flat RAG (9):** Analytical Engine (máy phân tích). Ada Lovelace đã tương tác với nó, từng dịch và chú thích bài viết về Analytical Engine. Cô cũng từng đến xem nguyên mẫu của Difference Engine trước đó.
**GraphRAG (10):** Analytical Engine.

### 9. Alfred Hitchcock works as FILM_DIRECTOR, SCREENWRITER, PRODUCER, EDITOR. Các vai trò của ông trong ngành điện ảnh là gì?
**GT:** FILM_DIRECTOR; SCREENWRITER; PRODUCER; EDITOR
**Flat Context:** Sir Alfred Joseph Hitchcock  (13 August 1899 – 29 April 1980) was an English film director, screenwriter, producer and editor. He is widely regarded as one of the most influential figures in the history of cinema. In a career spanning six decades, he directed over 50 feature films, many of which are...
**Graph Context:**
(Alfred Elton van Vogt)--[GRAND_MASTER_RANK]-->(14th)
(Alfred Hitchcock)--[WORKS_AS]-->(SCREENWRITER)
(Alfred Elton van Vogt)--[BORN_ON]-->(April 26, 1912)
(Alfred Elton van Vogt)--[GRAND_MASTER_BY_YEAR]-->(1995)
(Alfred Elton van Vogt)--[DIED_ON]-->(January 26, 2000)
(Alfred Hitchcock)--[WORKS_AS]-...
**Flat RAG (10):** Các vai trò của Alfred Hitchcock trong ngành điện ảnh là:

- Đạo diễn phim (Film Director): Chịu trách nhiệm sáng tạo và chỉ đạo tổng thể phim—lựa chọn diễn viên, hình ảnh, nhịp điệu và cách thể hiện câu chuyện trên màn ảnh.

- Người viết kịch bản (Screenwriter): Viết và/hoặc chỉnh sửa kịch bản, xây dựng cốt truyện và đối thoại, định hình cấu trúc phim.

- Nhà sản xuất (Producer): Quản lý sản xuất, bao gồm tài chính, lịch trình, nhân sự và các nguồn lực để dự án có thể hoàn tất.

- Người biên tập (Editor): Cắt ghép, sắp xếp cảnh quay, quyết định nhịp độ và trình tự để câu chuyện được kể mạch lạc và đạt hiệu quả nghệ thuật.

Hitchcock được biết đến là một trong những nhân vật có ảnh hưởng lớn nhất trong lịch sử điện ảnh, với sự đa năng ở những vai trò này.
**GraphRAG (10):** Các vai trò của Alfred Hitchcock trong ngành điện ảnh là:
- Đạo diễn phim (film director)
- Biên kịch (screenwriter)
- Nhà sản xuất (producer)
- Biên tập (editor)

### 10. Aruba IS_A CONSTITUENT_COUNTRY_OF_THE_KINGDOM_OF_THE_NETHERLANDS và Aruba BECAME_CONSTITUENT_COUNTRY_IN_YEAR 1986. Aruba trở thành nước thành phần của nước nào?
**GT:** Kingdom_of_the_NETHERLANDS
**Flat Context:** In August 1947, Aruba formulated its first Staatsreglement (constitution) for Aruba's status aparte as an autonomous state within the Kingdom of the Netherlands, prompted by the efforts of Henny Eman, a noted Aruban politician. By 1954, the Charter of the Kingdom of the Netherlands was established, ...
**Graph Context:**
(NEW_KINGDOM)--[RULED_OVER]-->(NUBIA)
(PTOLEMAIC_KINGDOM)--[EXISTED_UNTIL]-->(30_BC)
(American_Patriot_Forces)--[DEFEATED]-->(BRITISH)
(PTOLEMAIC_KINGDOM)--[FORMED_AFTER]-->(ALEXANDER_THE_GREAT_DEATH)
(Kingdom_of_Spain)--[SUPPORTS]-->(American_Patriot_Forces)
(Kingdom_of_France)--[SUPPORTS]-->(Ameri...
**Flat RAG (10):** Aruba là một nước thành phần của Vương quốc Hà Lan (Kingdom of the Netherlands).
**GraphRAG (10):** Aruba trở thành nước thành phần của Vương quốc Hà Lan (Kingdom of the Netherlands), vào năm 1986.

