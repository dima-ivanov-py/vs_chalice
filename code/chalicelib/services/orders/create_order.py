from chalicelib.services.base_service import BaseService


class CreateOrderService(BaseService):
    def __call__(self):
        self._data["amount"] = int(self._data["amount"])
        table = self.get_table()
        table.put_item(Item=self._data)
        return self._data
