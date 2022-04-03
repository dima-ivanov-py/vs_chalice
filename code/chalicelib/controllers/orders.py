from uuid import uuid4

from chalice import Response
from chalicelib.get_tables import get_orders_table
from chalicelib.models.orders.order_model import ORDER_STATUSES, OrderModel
from chalicelib.selectors.list_items import list_items_selector
from chalicelib.services.orders.create_order import CreateOrderService
from chalicelib.utils.username_getter import get_authorized_username
from pydantic import ValidationError


def create_order_response(request):
    data = {
        "username": get_authorized_username(request),
        "uid": str(uuid4()),
        "status": ORDER_STATUSES["pending"],
        "product_username": request.json_body.get("product_username"),
        "product_uid": request.json_body.get("product_uid"),
        "amount": request.json_body.get("amount"),
    }

    try:
        OrderModel.parse_obj(data)
    except ValidationError as e:
        return Response(
            body=e.json(),
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    create_service = CreateOrderService(table=get_orders_table(), data=data)
    result = create_service()

    return Response(
        body=result,
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


def list_orders_response(*, request):
    params = request.query_params
    table = get_orders_table()
    username = get_authorized_username(request)

    if params:
        return list_items_selector(
            table=table,
            username=username,
            next_=params.get("next"),
            back=params.get("back"),
        )

    return list_items_selector(table=table, username=username)
