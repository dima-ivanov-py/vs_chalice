from chalicelib.app import app
from chalicelib.auth.jwt_authorizer import jwt_auth
from chalicelib.controllers import users


@app.route("/users/all", methods=["GET"], authorizer=jwt_auth)
def list_user_all():
    return users.list_users_all_response(app.current_request)
