import datetime
import uuid
import jwt
import pytest
from proxy.jwt_manager import JWTManager
from proxy.settings import JWT_SIGNATURE_SECRET, JWT_SIGNATURE_ALGO


def test_generate_token():
    # Generate a token
    token = JWTManager.generate_token()

    # Ensure token is a string
    assert isinstance(token, str)

    # Decode the token to verify its structure
    payload = jwt.decode(token, JWT_SIGNATURE_SECRET,
                         algorithms=[JWT_SIGNATURE_ALGO])

    # Check 'iat'
    iat = payload.get("iat")
    assert iat is not None
    assert isinstance(iat, int)

    # Check 'jti'
    jti = payload.get("jti")
    assert jti is not None
    assert isinstance(jti, str)
    try:
        uuid.UUID(jti)
    except ValueError:
        pytest.fail(f"{jti} is not a valid UUID!")

    # Check 'payload'
    inner_payload = payload.get("payload")
    assert inner_payload is not None
    assert isinstance(inner_payload, dict)

    # Check 'user' in 'payload'
    user = inner_payload.get("user")
    assert user is not None
    assert user == "username"

    # Check 'date' in 'payload'
    date = inner_payload.get("date")
    assert date is not None
    today = datetime.datetime.today().date()
    assert date == str(today)
