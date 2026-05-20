from environs import Env
from loguru import logger

env = Env()
logger.info("Loading environment variables...")


DOPPLER_TOKEN = env.str("DOPPLER_TOKEN")
PROVIDER = env.str("PROVIDER")
