import json
import sys

import env
import requests
from loguru import logger


def main():
    provider = env.PROVIDER
    logger.info(f"Đang tiến hành cập nhật Payment Provider thành: {provider}")

    url = "https://api.doppler.com/v3/configs/config/secrets"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {env.DOPPLER_TOKEN}",
    }

    # Danh sách các môi trường cần cập nhật
    configs_to_update = ["dev", "prod"]
    has_error = False

    for config_name in configs_to_update:
        logger.info(f"Đang xử lý môi trường: {config_name}...")

        payload = json.dumps(
            {
                "project": "20206205tech",
                "config": config_name,
                "secrets": {"PAYMENT_DEFAULT_PROVIDER": provider},
            }
        )

        try:
            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                logger.success(f"[{config_name}] Cập nhật cấu hình thành công!")
            else:
                logger.error(
                    f"[{config_name}] Lỗi cập nhật. Mã HTTP: {response.status_code} - {response.text}"
                )
                has_error = True

        except Exception as e:
            logger.error(f"[{config_name}] Call API thất bại: {e}")
            has_error = True

    # Nếu có bất kỳ môi trường nào bị lỗi, thoát với code 1 để các pipeline CI/CD (nếu có) có thể catch được
    if has_error:
        logger.error(
            "Quá trình cập nhật hoàn tất nhưng có lỗi xảy ra. Vui lòng kiểm tra log ở trên."
        )
        sys.exit(1)
    else:
        logger.success("Đã cập nhật thành công toàn bộ các môi trường!")


if __name__ == "__main__":
    main()
