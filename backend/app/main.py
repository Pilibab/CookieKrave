from db.supabase_client import supabase

def test_connection():
    try:
        response = supabase.table("CUSTOMERS").select("*").limit(1).execute()
        print("✅ Connected to Supabase!")
        print("Data:", response.data)
    except Exception as e:
        print("❌ Connection failed")
        print("Error:", e)

test_connection()