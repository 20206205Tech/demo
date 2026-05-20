from environs import Env
from loguru import logger

env = Env()
logger.info("Loading environment variables...")

SUPABASE_PROJECT_ID = env.str("SUPABASE_PROJECT_ID")
SUPABASE_ANON_KEY = env.str("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = env.str("SUPABASE_SERVICE_ROLE_KEY")

SUPABASE_DB_PASSWORD = env.str("SUPABASE_DB_PASSWORD")

SUPABASE_DATABASE_URL = f"postgresql://aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?user=postgres.{SUPABASE_PROJECT_ID}&password={SUPABASE_DB_PASSWORD}"

EMAIL = env.str("EMAIL", "vuvannghia.work@gmail.com")
