from decimal import Decimal
from typing import Union

from pydantic import BaseModel


class UpdateProductModel(BaseModel):
    price: Union[Decimal, None]
    title: Union[str, None]
    uid: str
    username: str
