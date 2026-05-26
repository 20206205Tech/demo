import env
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Khởi tạo Database Engine và SessionLocal
engine = create_engine(env.DATA_PIPELINE_VBPLNEW_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_10_warning_documents():
    """Truy vấn 10 văn bản có trạng thái thuộc diện cần cảnh báo người dùng"""
    with SessionLocal() as db:
        query = text(
            """
            SELECT
                d.item_id,
                d.doc_num AS document_number,
                d.title,
                s.name AS status
            FROM documents d
            JOIN dim_eff_status s ON d.eff_status_id = s.id
            WHERE s.name IN :statuses
            LIMIT 10
            """
        )

        # Chuyển list thành tuple để SQLAlchemy hiểu cấu trúc IN (...)
        params = {"statuses": tuple(env.NO_SKIPPED_STATUS)}
        results = db.execute(query, params).fetchall()

        documents = [
            {"item_id": r[0], "document_number": r[1], "title": r[2], "status": r[3]}
            for r in results
        ]

        return documents


def main():
    logger.info(f"NO_SKIPPED_STATUS: {env.NO_SKIPPED_STATUS}")
    logger.info("Đang thực hiện truy vấn Database...")

    try:
        docs = get_10_warning_documents()

        if not docs:
            logger.warning("Không tìm thấy văn bản nào thỏa mãn điều kiện.")
        else:
            print("\n" + "=" * 60)
            print("DANH SÁCH 10 VĂN BẢN CẦN XÁC NHẬN (DEMO)")
            print("=" * 60 + "\n")

            for i, doc in enumerate(docs, 1):
                print(f"{i}: Tóm tắt nội dung của văn bản {doc['document_number']}")
                # print(f"   Trạng thái: {doc['status']}")
                # print(f"   Tiêu đề: {doc['title']}\n")
                # print("-" * 50)

    except Exception as e:
        logger.error(f"Đã xảy ra lỗi khi kết nối hoặc truy vấn DB: {e}")


if __name__ == "__main__":
    main()
