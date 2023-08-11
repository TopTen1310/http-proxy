import datetime
import jwt
from typing import Dict, Union
from .settings import JWT_SIGNATURE_ALGO, JWT_SIGNATURE_SECRET
import uuid


class JWTManager:
    @staticmethod
    def generate_token() -> str:
        payload: Dict[str, Union[datetime.datetime, Dict[str, str]]] = {
            "iat": datetime.datetime.utcnow(),
            "jti": str(uuid.uuid4()),
            "payload": {
                "user": "username",
                "date": str(datetime.datetime.today().date())
            }
        }
        token: str = jwt.encode(
            payload, JWT_SIGNATURE_SECRET, algorithm=JWT_SIGNATURE_ALGO)
        return token.decode() if isinstance(token, bytes) else token
