# dependencies/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.token import decode_token
from supabase import create_client, Client

SUPABASE_URL = "https://xoyzsjymkfcwtumzqzha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhveXpzanlta2Zjd3R1bXpxemhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMTk4MTUsImV4cCI6MjA1OTc5NTgxNX0.VLMHbn4-rMaz9DWK1zcIJccWBnaQhrepek-umKH2s0Y"
url = SUPABASE_URL
key = SUPABASE_KEY
supabase: Client = create_client(url, key)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    print(user_id)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Query Resource_Management_Admin using the global Supabase client
    response = supabase.table("Resource_Management_Admins").select("*").eq("user_id", user_id).execute()
    user_data = response.data

    if not user_data:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    return user_data[0]
