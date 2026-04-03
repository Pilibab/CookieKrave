from supabase import create_client
from config import configs

SUPABASE_URL = configs.SUPABASE_URL
SUPABASE_KEY = configs.SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY.get_secret_value())