import os

HOST_PORT = os.environ.get("HOST_PORT")
JWT_SIGNATURE_SECRET = os.environ.get("JWT_SIGNATURE_SECRET")
JWT_SIGNATURE_ALGO = os.environ.get("JWT_SIGNATURE_ALGO", "HS512")
JWT_HEADER_NAME = os.environ.get("JWT_HEADER_NAME", "x-my-jwt")
UPSTREAM_IP_OR_FQDN = os.environ.get("UPSTREAM_IP_OR_FQDN", "postman-echo.com")
UPSTREAM_PORT = os.environ.get("UPSTREAM_PORT", "443")
UPSTREAM_SCHEME = os.environ.get("UPSTREAM_SCHEME", "https")
URL_NOTATION = "{scheme}://{host}:{port}/{path}"
