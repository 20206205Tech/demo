from environs import Env
from loguru import logger

env = Env()
logger.info("Loading environment variables...")


DATA_PIPELINE_VBPLNEW_DATABASE_URL = env.str("DATA_PIPELINE_VBPLNEW_DATABASE_URL")


NO_SKIPPED_STATUS = [
    # 'Còn hiệu lực',
    # 'Không còn phù hợp',
    "Hết hiệu lực một phần",
    "Ngưng hiệu lực một phần",
    # 'Ngưng hiệu lực',
    "Chưa có hiệu lực",
    # 'Hết hiệu lực toàn bộ',
]
