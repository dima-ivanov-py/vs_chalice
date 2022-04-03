from chalicelib.app import app
from chalicelib.auth.jwt_authorizer import jwt_auth
from chalicelib.controllers import products


@app.route(
    "/products/of-user/{username}", methods=["GET"], authorizer=jwt_auth
)
def list_products_of_certain_user(username):
    return products.list_products_of_user(
        request=app.current_request, username=username
    )


@app.route("/products", methods=["GET"], authorizer=jwt_auth)
def list_products():
    return products.list_products_response(app.current_request)


@app.route("/products", methods=["POST"], authorizer=jwt_auth)
def create_product():
    return products.create_product_response(app.current_request)


@app.route("/products/{uid}", methods=["GET"], authorizer=jwt_auth)
def retrieve_product(uid):
    return products.retrieve_product_response(app.current_request, uid)


@app.route("/products/{uid}", methods=["PUT", "PATCH"], authorizer=jwt_auth)
def update_product(uid):
    return products.update_product_response(app.current_request, uid)


@app.route("/products/{uid}", methods=["DELETE"], authorizer=jwt_auth)
def delete_product(uid):
    return products.delete_product_response(app.current_request, uid)
