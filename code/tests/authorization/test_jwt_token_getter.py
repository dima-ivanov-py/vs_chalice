import pytest
from chalice import UnauthorizedError
from chalicelib.auth.auth_key_getter import get_auth_key
from chalicelib.auth.jwt_token_decoder import decode_jwt_token
from chalicelib.auth.jwt_token_getter import get_jwt_token


class TestJWTokenGetter:
    def test_get_token(self, users):
        user = users["users"]["user_0"]
        table = users["table"]
        username = user["username"]
        password = "password_0"  # noqa: S105
        record = table.get_item(Key={"username": username}).get("Item")
        auth_key = get_auth_key()
        jwt_token = get_jwt_token(
            username=username,
            password=password,
            auth_key=auth_key,
            record=record,
        )
        decoded = decode_jwt_token(token=jwt_token, auth_key=auth_key)
        assert decoded["sub"] == username

    def test_wrong_username(self, users):
        user = users["users"]["user_0"]
        table = users["table"]
        username = f"wrong_{user['username']}"
        password = "password_0"  # noqa: S105
        record = table.get_item(Key={"username": username}).get("Item")
        auth_key = get_auth_key()
        with pytest.raises(UnauthorizedError):
            get_jwt_token(
                username=username,
                password=password,
                auth_key=auth_key,
                record=record,
            )

    def test_wrong_password(self, users):
        user = users["users"]["user_0"]
        table = users["table"]
        username = user["username"]
        password = "wrong_password"  # noqa: S105
        record = table.get_item(Key={"username": username}).get("Item")
        auth_key = get_auth_key()
        with pytest.raises(UnauthorizedError):
            get_jwt_token(
                username=username,
                password=password,
                auth_key=auth_key,
                record=record,
            )
