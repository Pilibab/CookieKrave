from supabase import create_client
from config import configs

SUPABASE_URL = configs.SUPABASE_URL.get_secret_value()
SUPABASE_KEY = configs.SUPABASE_KEY.get_secret_value()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)