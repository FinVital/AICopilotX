
import os
from supabase import create_client, Client

url = "https://qadfjxzauvrjrfqahbbm.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhZGZqeHphdXZyanJmcWFoYmJtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxOTE0MDU0NiwiZXhwIjoyMDM0NzE2NTQ2fQ.kbDbfeuQp7LvVRJsaQ4K7MoE-qkxd0p4n3HA3GH-Db8"
supabase: Client = create_client(url, key)

def check():
    # Placeholder for fetching user data
    response = supabase.table("Record").select("*").execute()
    return response.data

def sign_up(user_id, name, email, password):
    # Placeholder for signing up user
    response = supabase.table("Record").insert({"id": user_id, "Name": name, "email": email, "Password": password}).execute()
    return response

def get_user_by_email(email):
    # Placeholder for fetching user by email
    response = supabase.table("Record").select("*").eq("email", email).execute()
    return response.data
