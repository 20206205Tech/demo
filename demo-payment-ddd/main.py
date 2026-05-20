import json
import sys

import env
import requests
from loguru import logger


def main():
    logger.info(f"Đang tiến hành cập nhật Payment Provider thành: {env.PROVIDER}")

    url = "https://api.doppler.com/v3/configs/config/secrets"

    payload = json.dumps(
        {
            "project": "20206205tech",
            "config": "prod",
            "secrets": {"PAYMENT_DEFAULT_PROVIDER": env.PROVIDER},
        }
    )

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {env.DOPPLER_TOKEN}",
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        # Kiểm tra HTTP status thay vì in toàn bộ response
        if response.status_code == 200:
            logger.success(f"Cập nhật cấu hình PAYMENT_DEFAULT_PROVIDER thành công!")
        else:
            logger.error(f"Lỗi cập nhật. Mã HTTP: {response.status_code}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Call API thất bại: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
