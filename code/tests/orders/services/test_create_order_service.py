from chalicelib.services.orders.create_order import CreateOrderService


class TestCreateOrderService:
    @staticmethod
    def _get_data():
        return {
            "username": "test_username",
            "uid": "test_uid",
            "status": "test_status",
            "product_username": "test_product_username",
            "product_uid": "test_product_uid",
            "amount": "2",
        }

    def test_create_order_with_valid_data(self, orders_table):
        data = self._get_data()
        create_service = CreateOrderService(table=orders_table, data=data)
        result = create_service()
        assert len(orders_table.scan()["Items"]) == 1
        assert result["amount"] == 2
