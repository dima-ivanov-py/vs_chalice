import jwt


def decode_jwt_token(*, token, auth_key):
    return jwt.decode(token, auth_key, algorithms=["HS256"])
