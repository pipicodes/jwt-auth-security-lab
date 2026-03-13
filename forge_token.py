import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

payload = {
    "sub": "alice",
    "role": "admin",
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(token)