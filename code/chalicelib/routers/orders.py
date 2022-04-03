from chalicelib.app import app
from chalicelib.auth.jwt_authorizer import jwt_auth
from chalicelib.controllers import orders


@app.route("/orders", methods=["GET"], authorizer=jwt_auth)
def list_orders():
    return orders.list_orders_response(request=app.current_request)


@app.route("/orders", methods=["POST"], authorizer=jwt_auth)
def create_order():
    return orders.create_order_response(request=app.current_request)
