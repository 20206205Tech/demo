import time

import env
import psycopg2
import pyotp


def main():
    print("🔌 Đang kết nối tới Supabase PostgreSQL...")

    try:
        # Mở kết nối tới database
        with psycopg2.connect(env.SUPABASE_DATABASE_URL) as conn:
            # Tạo cursor để thực thi SQL
            with conn.cursor() as cur:
                print("🔍 Đang truy vấn bảng auth.users để lấy ID...\n")

                # 1. Lấy ID của user dựa vào email
                cur.execute("SELECT id FROM auth.users WHERE email = %s;", (env.EMAIL,))
                user = cur.fetchone()

                if not user:
                    print(f"❌ Không tìm thấy người dùng nào với email: {env.EMAIL}")
                    return

                user_id = user[0]
                print(f"✅ Tìm thấy user_id: {user_id}")

                # 2. Lấy secret từ bảng auth.mfa_factors dựa vào user_id
                print("🔍 Đang truy vấn bảng auth.mfa_factors để lấy secret...")
                cur.execute(
                    "SELECT secret FROM auth.mfa_factors WHERE user_id = %s;",
                    (user_id,),
                )
                factor = cur.fetchone()

                if not factor:
                    print(f"❌ Không tìm thấy thông tin MFA cho user_id: {user_id}")
                    return

                secret = factor[0]
                print("✅ Đã lấy được MFA secret thành công.\n")

                # 3. Tính toán và in ra mã TOTP trong 5 phút (300 giây)
                totp = pyotp.TOTP(secret)
                print("⏳ Bắt đầu tạo mã TOTP (chạy liên tục trong 5 phút)...")
                print("-" * 50)

                end_time = time.time() + 300  # Thời gian kết thúc sau 5 phút

                while time.time() < end_time:
                    # Lấy mã 6 số hiện tại
                    current_code = totp.now()

                    # Tính toán số giây còn lại của mã hiện tại (TOTP thay đổi mỗi 30s)
                    valid_for = 30 - (int(time.time()) % 30)

                    # Tính thời gian tổng còn lại của chương trình
                    int(end_time - time.time())

                    print(
                        f"Mã TOTP: {current_code} (mã này sẽ hết hạn sau {valid_for}s)"
                    )

                    # Tạm dừng chương trình cho đến khi mã hiện tại hết hạn để tạo mã mới
                    time.sleep(valid_for)

        print("\n⏹️ Đã kết thúc chu trình 5 phút.")

    except psycopg2.Error as e:
        print(f"❌ Lỗi cơ sở dữ liệu: {e}")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()
