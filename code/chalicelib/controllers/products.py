from uuid import uuid4

from chalice import Response
from chalicelib.get_tables import get_products_table
from chalicelib.models.products.product_model import ProductModel
from chalicelib.models.products.update_product_model import UpdateProductModel
from chalicelib.selectors.get_product import get_product_selector
from chalicelib.selectors.list_items import list_items_selector
from chalicelib.services.products.create_product import CreateProductService
from chalicelib.services.products.delete_product import DeleteProductService
from chalicelib.services.products.update_product import UpdateProductService
from chalicelib.utils.username_getter import get_authorized_username
from pydantic import ValidationError


def list_products_of_user(*, request, username: str):
    params = request.query_params
    table = get_products_table()

    if params:
        return list_items_selector(
            table=table,
            username=username,
            next_=params.get("next"),
            back=params.get("back"),
        )

    return list_items_selector(table=table, username=username)


def list_products_response(request):
    params = request.query_params
    table = get_products_table()
    username = get_authorized_username(request)

    if params:
        return list_items_selector(
            table=table,
            username=username,
            next_=params.get("next"),
            back=params.get("back"),
        )

    return list_items_selector(table=table, username=username)


def create_product_response(request):
    data = {
        "title": request.json_body.get("title"),
        "price": request.json_body.get("price"),
        "username": get_authorized_username(request),
        "uid": str(uuid4()),
    }

    try:
        ProductModel.parse_obj(data)
    except ValidationError as e:
        return Response(
            body=e.json(),
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    create_service = CreateProductService(
        table=get_products_table(), data=data
    )
    result = create_service()

    return Response(
        body=result,
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


def retrieve_product_response(request, uid):
    table = get_products_table()
    username = get_authorized_username(request)
    try:
        data = get_product_selector(table=table, uid=uid, username=username)
    except KeyError:
        return Response(
            body=None,
            status_code=404,
            headers={"Content-Type": "application/json"},
        )
    ProductModel.parse_obj(data)
    return data


def update_product_response(request, uid):
    data = {
        "title": request.json_body.get("title"),
        "price": request.json_body.get("price"),
        "username": get_authorized_username(request),
        "uid": uid,
    }

    try:
        UpdateProductModel.parse_obj(data)
    except ValidationError as e:
        return Response(
            body=e.json(),
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    update_service = UpdateProductService(
        table=get_products_table(), data=data
    )
    result = update_service()

    if result:
        return result

    return Response(
        body=None,
        status_code=404,
        headers={"Content-Type": "application/json"},
    )


def delete_product_response(request, uid):
    delete_service = DeleteProductService(
        table=get_products_table(),
        uid=uid,
        username=get_authorized_username(request),
    )
    deleted = delete_service()

    if deleted:
        return Response(
            body={},
            status_code=204,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        body=None,
        status_code=404,
        headers={"Content-Type": "application/json"},
    )
