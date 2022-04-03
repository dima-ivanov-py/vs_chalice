from decimal import Decimal

from chalicelib.services.base_service import BaseService


class CreateProductService(BaseService):
    def __call__(self):
        self._data["price"] = round(Decimal(self._data["price"]), 2)
        table = self.get_table()
        table.put_item(Item=self._data)
        return self._data
