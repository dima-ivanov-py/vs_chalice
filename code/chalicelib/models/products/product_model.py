from decimal import Decimal

from pydantic import BaseModel


class ProductModel(BaseModel):
    price: Decimal
    title: str
    uid: str
    username: str
