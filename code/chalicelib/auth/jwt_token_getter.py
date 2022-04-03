import datetime
import hashlib
import hmac
from typing import Any, Dict
from uuid import uuid4

import jwt
from chalice import UnauthorizedError


def get_jwt_token(
    *, username: str, password: str, auth_key: bytes, record: Dict[str, Any]
) -> str:
    if record is None:
        raise UnauthorizedError("Invalid username or password")

    actual = hashlib.pbkdf2_hmac(
        record["hash"],
        password.encode("utf-8"),
        record["salt"].value,
        int(record["rounds"]),
    )

    expected = record["hashed"].value

    if not hmac.compare_digest(actual, expected):
        raise UnauthorizedError("Invalid username or password")

    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(days=1)  # noqa: F841

    payload = {
        "sub": username,
        "iat": now,
        "nbf": now,
        "jti": str(uuid4()),
        # "exp": exp,  noqa: E800
    }

    return jwt.encode(payload, auth_key, algorithm="HS256")
