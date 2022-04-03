from chalice import AuthResponse
from chalicelib.app import app
from chalicelib.auth.auth_key_getter import get_auth_key
from chalicelib.auth.jwt_token_decoder import decode_jwt_token
from chalicelib.config import DEFAULT_USERNAME
from jwt import DecodeError, InvalidSignatureError


@app.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token
    auth_key = get_auth_key()

    try:
        decoded = decode_jwt_token(token=token, auth_key=auth_key)
        return AuthResponse(routes=["*"], principal_id=decoded["sub"])
    except (InvalidSignatureError, DecodeError):
        return AuthResponse(routes=[], principal_id=DEFAULT_USERNAME)
