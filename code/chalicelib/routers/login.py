from chalicelib.app import app
from chalicelib.controllers.login import login_response


@app.route("/login", methods=["POST"])
def login():
    return login_response(app.current_request)
