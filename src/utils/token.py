from jose import JWTError, jwt

SECRET_KEY = "be14be2aaab20c580d07eb9fc5038b5f7d35ec59243caed20c130ff13ba06874"
ALGORITHM = "HS256"

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except JWTError:
        return None
