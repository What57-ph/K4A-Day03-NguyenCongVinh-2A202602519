"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                # TODO 1.2: Khai báo các thuộc tính tham số cho Tool tại đây...
            },
            "required": [] # TODO 1.2: Khai báo danh sách các trường bắt buộc tại đây...
        }
    }
]

TOOLS_SCHEMA_HR_SUPPORT = [
    {
        "name": "job_criteria_lookup",
        "description": "Tra cứu tiêu chí, yêu cầu và thông tin chi tiết của một vị trí tuyển dụng đang mở.",
        "parameters": {
            "type": "object",
            "properties": {
                "position_name": {
                    "type": "string",
                    "description": "Tên vị trí cần tra cứu (ví dụ: 'Backend Java Developer')"
                },
                "department": {
                    "type": "string",
                    "description": "Phòng ban của vị trí, nếu có (ví dụ: 'Engineering')"
                }
            },
            "required": ["position_name"]
        }
    },
    {
        "name": "parse_cv",
        "description": "Trích xuất thông tin có cấu trúc (kỹ năng, kinh nghiệm, học vấn, thông tin liên hệ) từ file CV của ứng viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "cv_file_url": {
                    "type": "string",
                    "description": "Đường dẫn/URL tới file CV cần phân tích (PDF hoặc DOCX)"
                }
            },
            "required": ["cv_file_url"]
        }
    },
    {
        "name": "score_cv_against_position",
        "description": "So khớp thông tin CV đã trích xuất với tiêu chí của một vị trí, trả về điểm phù hợp và giải trình theo từng tiêu chí.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần chấm điểm"
                },
                "position_id": {
                    "type": "string",
                    "description": "Mã vị trí tuyển dụng dùng làm chuẩn so khớp"
                }
            },
            "required": ["candidate_id", "position_id"]
        }
    },
    {
        "name": "get_candidate_status",
        "description": "Tra cứu trạng thái hiện tại của một ứng viên trong quy trình tuyển dụng. Có thể tra theo mã ứng viên, theo họ tên, hoặc cả hai để tăng độ chính xác.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần tra cứu (ví dụ: 'CV2026001'). Bỏ trống nếu chỉ biết tên."
                },
                "full_name": {
                    "type": "string",
                    "description": "Họ tên ứng viên cần tra cứu (ví dụ: 'Trần Thị Bình'). Bỏ trống nếu chỉ biết mã."
                }
            },
            "required": []
        }
    },
    {
        "name": "check_interviewer_availability",
        "description": "Kiểm tra các khung giờ trống trên lịch của phỏng vấn viên hoặc HR trong một khoảng thời gian nhất định.",
        "parameters": {
            "type": "object",
            "properties": {
                "interviewer_id": {
                    "type": "string",
                    "description": "Mã nhân viên/phỏng vấn viên cần kiểm tra lịch"
                },
                "date_from": {
                    "type": "string",
                    "description": "Ngày bắt đầu khoảng thời gian cần kiểm tra (định dạng YYYY-MM-DD)"
                },
                "date_to": {
                    "type": "string",
                    "description": "Ngày kết thúc khoảng thời gian cần kiểm tra (định dạng YYYY-MM-DD)"
                }
            },
            "required": ["interviewer_id", "date_from", "date_to"]
        }
    },
    {
        "name": "schedule_interview",
        "description": "Tạo lịch phỏng vấn cho ứng viên với phỏng vấn viên tại một khung giờ cụ thể, đồng thời tạo sự kiện trên lịch.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên được mời phỏng vấn"
                },
                "interviewer_id": {
                    "type": "string",
                    "description": "Mã phỏng vấn viên phụ trách buổi phỏng vấn"
                },
                "interview_time": {
                    "type": "string",
                    "description": "Thời gian phỏng vấn (định dạng ISO 8601, ví dụ: '2026-09-20T09:00:00')"
                },
                "location": {
                    "type": "string",
                    "description": "Địa điểm hoặc link phỏng vấn online, nếu có"
                }
            },
            "required": ["candidate_id", "interviewer_id", "interview_time"]
        }
    },
    {
        "name": "send_notification",
        "description": "Gửi thông báo (lịch phỏng vấn, kết quả sàng lọc, nhắc lịch) tới ứng viên hoặc nhân sự qua kênh chỉ định.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient_id": {
                    "type": "string",
                    "description": "Mã ứng viên hoặc nhân viên nhận thông báo"
                },
                "channel": {
                    "type": "string",
                    "enum": ["email", "sms", "zalo", "push", "in_app"],
                    "description": "Kênh gửi thông báo"
                },
                "message_type": {
                    "type": "string",
                    "enum": ["interview_invite", "interview_reminder", "screening_result", "rejection"],
                    "description": "Loại thông báo cần gửi"
                },
                "content": {
                    "type": "string",
                    "description": "Nội dung tùy chỉnh thêm cho thông báo, nếu có"
                }
            },
            "required": ["recipient_id", "channel", "message_type"]
        }
    },
    {
        "name": "update_candidate_status",
        "description": "Cập nhật trạng thái ứng viên trong quy trình tuyển dụng sau mỗi bước xử lý.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần cập nhật trạng thái"
                },
                "new_status": {
                    "type": "string",
                    "enum": ["screened", "interview_scheduled", "interviewed", "hired", "rejected"],
                    "description": "Trạng thái mới của ứng viên"
                }
            },
            "required": ["candidate_id", "new_status"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

# ============================================================
# MOCK DATABASE — Trợ lý Tuyển dụng & Sàng lọc CV
# ============================================================

# 1. Vị trí tuyển dụng (dùng cho job_criteria_lookup, score_cv_against_position)
JOB_POSITIONS = {
    "POS2026001": {
        "position_name": "Backend Java Developer",
        "department": "Engineering",
        "level": "Mid-level",
        "required_skills": ["Java", "Spring Boot", "Microservices", "SQL"],
        "preferred_skills": ["Docker", "Kubernetes", "Kafka"],
        "min_experience_years": 2,
        "education_requirement": "Cử nhân CNTT hoặc tương đương",
        "salary_range": "20-35 triệu VNĐ",
        "status": "Đang tuyển"
    },
    "POS2026002": {
        "position_name": "AI Engineer (RAG/LLM)",
        "department": "Product",
        "level": "Junior-Mid",
        "required_skills": ["Python", "FastAPI", "LLM", "Vector DB"],
        "preferred_skills": ["LangChain", "Claude API", "pgvector"],
        "min_experience_years": 1,
        "education_requirement": "Cử nhân CNTT/AI hoặc tương đương",
        "salary_range": "18-30 triệu VNĐ",
        "status": "Đang tuyển"
    }
}

# 2. Ứng viên & CV đã trích xuất (dùng cho parse_cv, score_cv_against_position, get/update_candidate_status)
CANDIDATES = {
    "CV2026001": {
        "full_name": "Nguyễn Văn An",
        "email": "an.nv@gmail.com",
        "phone": "0901234567",
        "cv_file_url": "https://storage.antigravity.vn/cv/CV2026001.pdf",
        "applied_position_id": "POS2026001",
        "extracted_skills": ["Java", "Spring Boot", "MySQL", "Docker"],
        "experience_years": 2.5,
        "education": "Cử nhân CNTT - Đại học Bách Khoa",
        "match_score": 88,
        "score_explanation": "Đạt 3/4 kỹ năng bắt buộc, có kinh nghiệm Docker (kỹ năng ưu tiên), đủ số năm kinh nghiệm yêu cầu.",
        "status": "interview_scheduled"
    },
    "CV2026002": {
        "full_name": "Trần Thị Bình",
        "email": "binh.tt@gmail.com",
        "phone": "0912345678",
        "cv_file_url": "https://storage.antigravity.vn/cv/CV2026002.pdf",
        "applied_position_id": "POS2026002",
        "extracted_skills": ["Python", "FastAPI", "Pandas"],
        "experience_years": 0.5,
        "education": "Cử nhân Khoa học Máy tính - VinUni",
        "match_score": 55,
        "score_explanation": "Thiếu kinh nghiệm với LLM/Vector DB, số năm kinh nghiệm dưới yêu cầu tối thiểu.",
        "status": "screened"
    }
}

# 3. Phỏng vấn viên & lịch trống (dùng cho check_interviewer_availability, schedule_interview)
INTERVIEWERS = {
    "EMP001": {
        "full_name": "Lê Văn Cường",
        "role": "Engineering Manager",
        "department": "Engineering",
        "email": "cuong.lv@antigravity.vn",
        "busy_slots": [
            {"start": "2026-09-20T09:00:00", "end": "2026-09-20T10:00:00"},
            {"start": "2026-09-21T14:00:00", "end": "2026-09-21T15:00:00"}
        ]
    },
    "EMP002": {
        "full_name": "Phạm Thị Dung",
        "role": "HR Manager",
        "department": "HR",
        "email": "dung.pt@antigravity.vn",
        "busy_slots": [
            {"start": "2026-09-20T10:00:00", "end": "2026-09-20T11:00:00"}
        ]
    }
}

# 4. Lịch phỏng vấn đã tạo (dùng cho schedule_interview)
INTERVIEW_SCHEDULE = {
    "INT2026001": {
        "candidate_id": "CV2026001",
        "interviewer_id": "EMP001",
        "interview_time": "2026-09-22T09:00:00",
        "location": "https://meet.google.com/abc-defg-hij",
        "status": "confirmed"
    }
}

# 5. Nhật ký thông báo đã gửi (dùng cho send_notification)
NOTIFICATION_LOG = {
    "NOTI2026001": {
        "recipient_id": "CV2026001",
        "channel": "email",
        "message_type": "interview_invite",
        "content": "Bạn được mời phỏng vấn vị trí Backend Java Developer lúc 09:00 ngày 22/09/2026.",
        "sent_at": "2026-09-15T08:30:00",
        "delivery_status": "delivered"
    }
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
# TOOL_ROUTER = {
#     "academic_query": execute_academic_query,
#     "schedule_appointment": execute_schedule_appointment
# }

# def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
#     """Hàm trung chuyển thực thi tool"""
#     if tool_name in TOOL_ROUTER:
#         try:
#             return TOOL_ROUTER[tool_name](**arguments)
#         except Exception as e:
#             return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
#     return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)

import json
from typing import Dict, Any
from datetime import datetime


def execute_job_criteria_lookup(position_name: str, department: str = None) -> str:
    """Thực thi tra cứu tiêu chí tuyển dụng theo tên vị trí (và phòng ban nếu có)"""
    position_name_norm = position_name.strip().lower()
    matches = [
        {**pos, "position_id": pid}
        for pid, pos in JOB_POSITIONS.items()
        if position_name_norm in pos["position_name"].lower()
        and (department is None or pos["department"].lower() == department.strip().lower())
    ]
    if matches:
        return json.dumps({
            "status": "SUCCESS",
            "count": len(matches),
            "data": matches
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy vị trí tuyển dụng nào khớp với '{position_name}'"
        }, ensure_ascii=False)


def execute_parse_cv(cv_file_url: str) -> str:
    """Thực thi trích xuất thông tin CV theo URL file"""
    candidate = next(
        (dict(c, candidate_id=cid) for cid, c in CANDIDATES.items() if c["cv_file_url"] == cv_file_url),
        None
    )
    if candidate:
        return json.dumps({
            "status": "SUCCESS",
            "data": {
                "candidate_id": candidate["candidate_id"],
                "full_name": candidate["full_name"],
                "extracted_skills": candidate["extracted_skills"],
                "experience_years": candidate["experience_years"],
                "education": candidate["education"]
            }
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy hoặc chưa xử lý được file CV tại '{cv_file_url}'"
        }, ensure_ascii=False)


def execute_score_cv_against_position(candidate_id: str, position_id: str) -> str:
    """Thực thi chấm điểm phù hợp giữa CV ứng viên và một vị trí tuyển dụng"""
    candidate = CANDIDATES.get(candidate_id.strip().upper())
    position = JOB_POSITIONS.get(position_id.strip().upper())

    if not candidate:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy ứng viên có mã '{candidate_id}'"
        }, ensure_ascii=False)
    if not position:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy vị trí tuyển dụng có mã '{position_id}'"
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "candidate_id": candidate_id,
        "position_id": position_id,
        "match_score": candidate["match_score"],
        "explanation": candidate["score_explanation"]
    }, ensure_ascii=False)


def execute_get_candidate_status(candidate_id: str = None, full_name: str = None) -> str:
    """Thực thi tra cứu trạng thái hiện tại của ứng viên theo mã, theo tên, hoặc cả hai"""
    if not candidate_id and not full_name:
        return json.dumps({
            "status": "EXECUTION_ERROR",
            "error": "Cần cung cấp ít nhất candidate_id hoặc full_name để tra cứu."
        }, ensure_ascii=False)

    cid_norm = candidate_id.strip().upper() if candidate_id else None
    name_norm = full_name.strip().lower() if full_name else None

    candidate = None
    found_id = None

    if cid_norm:
        candidate = CANDIDATES.get(cid_norm)
        found_id = cid_norm

    if not candidate and name_norm:
        for cid, c in CANDIDATES.items():
            if name_norm in c["full_name"].lower():
                candidate = c
                found_id = cid
                break

    if candidate:
        return json.dumps({
            "status": "SUCCESS",
            "candidate_id": found_id,
            "full_name": candidate["full_name"],
            "current_status": candidate["status"]
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu ứng viên khớp với candidate_id='{candidate_id}' / full_name='{full_name}'"
        }, ensure_ascii=False)


def execute_check_interviewer_availability(interviewer_id: str, date_from: str, date_to: str) -> str:
    """Thực thi kiểm tra lịch trống của phỏng vấn viên trong khoảng thời gian"""
    interviewer = INTERVIEWERS.get(interviewer_id.strip().upper())
    if not interviewer:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phỏng vấn viên có mã '{interviewer_id}'"
        }, ensure_ascii=False)

    try:
        d_from = datetime.fromisoformat(date_from)
        d_to = datetime.fromisoformat(date_to)
    except ValueError:
        return json.dumps({
            "status": "EXECUTION_ERROR",
            "error": "date_from/date_to phải theo định dạng YYYY-MM-DD"
        }, ensure_ascii=False)

    busy_in_range = [
        slot for slot in interviewer["busy_slots"]
        if d_from <= datetime.fromisoformat(slot["start"]) <= d_to
    ]
    return json.dumps({
        "status": "SUCCESS",
        "interviewer_id": interviewer_id,
        "full_name": interviewer["full_name"],
        "busy_slots_in_range": busy_in_range,
        "message": "Ngoài các khung giờ bận nêu trên, phỏng vấn viên đang trống lịch."
    }, ensure_ascii=False)


def execute_schedule_interview(candidate_id: str, interviewer_id: str, interview_time: str, location: str = "Online - link sẽ gửi sau") -> str:
    """Thực thi tạo lịch phỏng vấn cho ứng viên"""
    candidate = CANDIDATES.get(candidate_id.strip().upper())
    interviewer = INTERVIEWERS.get(interviewer_id.strip().upper())

    if not candidate:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy ứng viên có mã '{candidate_id}'"
        }, ensure_ascii=False)
    if not interviewer:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phỏng vấn viên có mã '{interviewer_id}'"
        }, ensure_ascii=False)

    booking_id = f"INT-{candidate_id}-{len(INTERVIEW_SCHEDULE) + 1:03d}"
    INTERVIEW_SCHEDULE[booking_id] = {
        "candidate_id": candidate_id,
        "interviewer_id": interviewer_id,
        "interview_time": interview_time,
        "location": location,
        "status": "confirmed"
    }
    candidate["status"] = "interview_scheduled"

    return json.dumps({
        "status": "SUCCESS",
        "booking_id": booking_id,
        "candidate_id": candidate_id,
        "interviewer": interviewer["full_name"],
        "interview_time": interview_time,
        "location": location,
        "message": f"Đặt lịch phỏng vấn thành công cho {candidate['full_name']} với {interviewer['full_name']} lúc {interview_time}."
    }, ensure_ascii=False)


def execute_send_notification(recipient_id: str, channel: str, message_type: str, content: str = None) -> str:
    """Thực thi gửi thông báo tới ứng viên hoặc nhân sự"""
    candidate = CANDIDATES.get(recipient_id.strip().upper())
    interviewer = INTERVIEWERS.get(recipient_id.strip().upper())
    recipient_name = candidate["full_name"] if candidate else (interviewer["full_name"] if interviewer else None)

    if not recipient_name:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy người nhận có mã '{recipient_id}'"
        }, ensure_ascii=False)

    notification_id = f"NOTI{len(NOTIFICATION_LOG) + 2026001:07d}"
    NOTIFICATION_LOG[notification_id] = {
        "recipient_id": recipient_id,
        "channel": channel,
        "message_type": message_type,
        "content": content or f"[{message_type}] Thông báo tự động gửi tới {recipient_name}",
        "sent_at": datetime.now().isoformat(timespec="seconds"),
        "delivery_status": "delivered"
    }

    return json.dumps({
        "status": "SUCCESS",
        "notification_id": notification_id,
        "recipient": recipient_name,
        "channel": channel,
        "message": f"Đã gửi thông báo '{message_type}' tới {recipient_name} qua {channel}."
    }, ensure_ascii=False)


def execute_update_candidate_status(candidate_id: str, new_status: str) -> str:
    """Thực thi cập nhật trạng thái ứng viên trong quy trình tuyển dụng"""
    candidate = CANDIDATES.get(candidate_id.strip().upper())
    if not candidate:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy ứng viên có mã '{candidate_id}'"
        }, ensure_ascii=False)

    old_status = candidate["status"]
    candidate["status"] = new_status
    return json.dumps({
        "status": "SUCCESS",
        "candidate_id": candidate_id,
        "old_status": old_status,
        "new_status": new_status,
        "message": f"Cập nhật trạng thái ứng viên {candidate['full_name']} từ '{old_status}' sang '{new_status}' thành công."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "job_criteria_lookup": execute_job_criteria_lookup,
    "parse_cv": execute_parse_cv,
    "score_cv_against_position": execute_score_cv_against_position,
    "get_candidate_status": execute_get_candidate_status,
    "check_interviewer_availability": execute_check_interviewer_availability,
    "schedule_interview": execute_schedule_interview,
    "send_notification": execute_send_notification,
    "update_candidate_status": execute_update_candidate_status
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
