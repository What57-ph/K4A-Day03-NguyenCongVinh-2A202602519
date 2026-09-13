# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Điền Họ và Tên]  
> **Mã Sinh Viên / Mã Học viên:** [Điền MSSV]  
> **Chủ đề Lựa chọn:** [Điền tên chủ đề đã chọn từ docs/DANH_SACH_DE_TAI.md hoặc Đề tài Mở]

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá           | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm                                                                                                                                                                     |
| :-------------------------- | :------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Multi-step Reasoning** |     4 / 5      | Quy trình gồm nhiều bước nối tiếp: đọc JD → trích xuất tiêu chí → parse CV ứng viên → so khớp từng tiêu chí → tính điểm phù hợp → ra quyết định (đạt/không đạt) → soạn và gửi thông báo lịch phỏng vấn. |
| **2. Tool Interaction**     |     5 / 5      | Hệ thống có cần kết nối với CSDL để tìm và đọc CV cho vị trí tuyển dụng, gọi tool parse CV, hệ thống lập lịch(Google Calendar), hệ thống thông báo(SMS, Email, ...)                                     |
| **3. Dynamic Decision**     |     3 / 5      | Cần quyết định CV đủ điều kiện đáp ứng (pass -> soạn mail pass, lập lịch, gửi thông báo/ fail -> báo reject CV/lưu hồ sơ)                                                                               |
| **4. Long Horizon Goal**    |     3 / 5      | Mục tiêu tổng là tuyển ứng viên cần được giữ xuyên suốt qua nhiều CV và nhiều vòng, nhưng mỗi phiên xử lý một CV tương đối độc lập, không đòi hỏi trạng thái dài hạn phức tạp.                          |
| **TỔNG ĐIỂM AGENTIC FIT**   |  **15 / 20**   | _Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System._                                                                                                                                |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Đặt lịch phỏng vấn cho ứng viên Trần Thị Bình với mã ứng viên POS2026002, mã phỏng vấn viên EMP001, thời gian từ 9 giờ sáng 20-09-2026 đến 9h30 sáng cùng ngày",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "check_interviewer_availability",
    "arguments": {
      "interviewer_id": "EMP001",
      "date_from": "2026-09-20",
      "date_to": "2026-09-20"
    },
    "observation": {
      "status": "SUCCESS",
      "interviewer_id": "EMP001",
      "full_name": "Lê Văn Cường",
      "busy_slots_in_range": [],
      "message": "Ngoài các khung giờ bận nêu trên, phỏng vấn viên đang trống lịch."
    },
    "latency_ms": 2474.86
  },
  {
    "step": 2,
    "query": "Đặt lịch phỏng vấn cho ứng viên Trần Thị Bình với mã ứng viên POS2026002, mã phỏng vấn viên EMP001, thời gian từ 9 giờ sáng 20-09-2026 đến 9h30 sáng cùng ngày",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Ngoài các khung giờ bận nêu trên, phỏng vấn viên đang trống lịch.",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
