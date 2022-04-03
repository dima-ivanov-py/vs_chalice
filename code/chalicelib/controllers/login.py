from chalicelib.auth.auth_key_getter import get_auth_key
from chalicelib.auth.jwt_token_getter import get_jwt_token
from chalicelib.get_tables import get_users_table


def login_response(request):
    body = request.json_body
    username = body["username"]
    password = body["password"]
    record = get_users_table().get_item(Key={"username": username}).get("Item")
    auth_key = get_auth_key()
    jwt_token = get_jwt_token(
        username=username, password=password, auth_key=auth_key, record=record
    )
    return {"token": jwt_token}
