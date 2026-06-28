import os

from environs import Env
from loguru import logger

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)
# Configure loguru to write to a log file in the logs/ folder
logger.add("logs/run.log", rotation="10 MB", encoding="utf-8", level="INFO")

env = Env()
logger.info("Loading environment variables...")

SUPABASE_PROJECT_ID = env.str("SUPABASE_PROJECT_ID", default="")
SUPABASE_ANON_KEY = env.str("SUPABASE_ANON_KEY", default="")
SUPABASE_SERVICE_ROLE_KEY = env.str("SUPABASE_SERVICE_ROLE_KEY", default="")

SUPABASE_DB_PASSWORD = env.str("SUPABASE_DB_PASSWORD", default="")

if SUPABASE_PROJECT_ID and SUPABASE_DB_PASSWORD:
    SUPABASE_DATABASE_URL = f"postgresql://aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?user=postgres.{SUPABASE_PROJECT_ID}&password={SUPABASE_DB_PASSWORD}"
else:
    SUPABASE_DATABASE_URL = ""

EMAIL = env.str("EMAIL", "vuvannghia.work@gmail.com")
TOKEN = env.str("TOKEN")
