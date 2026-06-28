import json
import time
from datetime import datetime

# Import env to ensure environment variables are loaded and loguru is configured
from data import TEST_CASES
from format_sources import format_sources
from loguru import logger
from start_new_chat import start_new_chat
from stream_chat_response import stream_chat_response


def main():
    logger.info("=" * 60)
    logger.info("BẮT ĐẦU CHẠY THỬ NGHIỆM ĐÁNH GIÁ HỆ THỐNG RAG (CÓ ĐỘ TRỄ 2 PHÚT)")
    logger.info("=" * 60)

    results = []
    result_file_path = "result.json"

    for idx, tc in enumerate(TEST_CASES):
        logger.info(
            f"[Test Case {tc['id']}/{len(TEST_CASES)}] Phân loại: {tc['category']}"
        )
        logger.info(f"-> Câu hỏi: \"{tc['query']}\"")

        start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Bước 1: Khởi tạo phiên chat mới
            logger.info("   Đang tạo phiên chat mới...")
            chat_id = start_new_chat()
            logger.info(f"   Đã tạo Chat ID: {chat_id}")

            # Bước 2: Gửi câu hỏi và nhận phản hồi
            logger.info("   Đang gửi yêu cầu và nhận phản hồi...")
            start_time = time.time()
            answer, sources = stream_chat_response(chat_id, tc["query"])
            latency = time.time() - start_time

            logger.info(f"   Hoàn thành sau {latency:.2f} giây")

            # Định dạng nguồn tài liệu và câu trả lời
            formatted_ctx = format_sources(sources)

            # Lưu thông tin chi tiết của test case
            case_result = {
                "stt": tc["id"],
                "phan_loai": tc["category"],
                "cau_hoi": tc["query"],
                "tai_lieu_raw": sources,
                "tai_lieu_formatted": formatted_ctx,
                "cau_tra_loi": answer,
                "thoi_gian_bat_dau": start_timestamp,
                "thoi_gian_xu_ly": f"{latency:.2f}s",
                "trang_thai": "Thành công",
            }
            results.append(case_result)

        except Exception as e:
            logger.error(f"   [LỖI] Không thể hoàn thành test case này: {e}")
            case_result = {
                "stt": tc["id"],
                "phan_loai": tc["category"],
                "cau_hoi": tc["query"],
                "tai_lieu_raw": [],
                "tai_lieu_formatted": "N/A",
                "cau_tra_loi": f"Lỗi hệ thống: {str(e)}",
                "thoi_gian_bat_dau": start_timestamp,
                "thoi_gian_xu_ly": "N/A",
                "trang_thai": f"Lỗi: {str(e)}",
            }
            results.append(case_result)

        # Ghi đè file result.json sau mỗi test case đề phòng sự cố gián đoạn
        try:
            with open(result_file_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            logger.info(f"   Đã lưu/cập nhật kết quả vào {result_file_path}")
        except Exception as write_err:
            logger.error(f"   [LỖI] Không thể ghi file {result_file_path}: {write_err}")

        # Đợi 2 phút trước khi tiếp tục câu tiếp theo (trừ câu cuối cùng)
        if idx < len(TEST_CASES) - 1:
            wait_seconds = 120
            logger.info(
                f"   [CHỜ] Đang chờ {wait_seconds} giây (2 phút) để tránh giới hạn API LLM..."
            )
            time.sleep(wait_seconds)

    logger.info("=" * 60)
    logger.info(
        f"HOÀN THÀNH TẤT CẢ TEST CASES. KẾT QUẢ ĐÃ ĐƯỢC LƯU TẠI: {result_file_path}"
    )
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
