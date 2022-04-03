from chalicelib.selectors.get_product import get_product_selector
from chalicelib.services.base_service import BaseService


class DeleteProductService(BaseService):
    def __init__(self, *, table, uid: str = None, username: str = None):
        super().__init__(table=table)
        self._uid = uid
        self._username = username

    def set_uid(self, *, uid):
        self._uid = uid

    def set_username(self, *, username):
        self._username = username

    def __call__(self) -> bool:
        table = self.get_table()

        try:
            item = get_product_selector(
                table=table, uid=self._uid, username=self._username
            )
        except KeyError:
            return False

        table.delete_item(
            Key={"username": item["username"], "uid": item["uid"]}
        )
        return True
