from decimal import Decimal
from typing import Any, Dict

from chalicelib.selectors.get_product import get_product_selector
from chalicelib.services.base_service import BaseService


class UpdateProductService(BaseService):
    def __init__(self, *, table, data: Dict[str, Any] = None) -> None:
        super().__init__(table=table)
        self._data = data

    def set_data(self, *, data: Dict[str, Any]) -> None:
        self._data = data

    def __call__(self):
        table = self.get_table()
        try:
            item = get_product_selector(
                table=table,
                uid=self._data["uid"],
                username=self._data["username"],
            )
        except KeyError:
            return None

        title = self._data["title"]
        price = self._data["price"]

        if title:
            item["title"] = title

        if price:
            item["price"] = price

        item["price"] = round(Decimal(float(item["price"])), 2)

        table.put_item(Item=item)

        return item
