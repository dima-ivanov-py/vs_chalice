from chalicelib.services.products.delete_product import DeleteProductService


class TestDeleteProductAPI:
    @staticmethod
    def run_test(
        *,
        token,
        client,
        mocker,
        monkeypatch,
        product,
        table,
        path: str = "/products",
        uid: str,
        headers=None,
    ):
        def get_test_table(*args, **kwargs):
            return table

        monkeypatch.setattr(DeleteProductService, "get_table", get_test_table)
        mocker.patch(
            "chalicelib.controllers.products.get_authorized_username",
            return_value=product["username"],
        )

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Authorization": token,
            }

        return client.http.delete(
            path=f"{path}/{uid}", headers=headers, body=None
        )

    def test_can_delete_product(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        product = products["products_of_user_1"]["product_1"]
        response_1 = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            uid=product["uid"],
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=products["table"],
        )

        response_2 = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            uid=product["uid"],
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=products["table"],
        )

        assert response_1.status_code == 204
        assert response_2.status_code == 404

    def test_wrong_uid(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        product = products["products_of_user_1"]["product_1"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            uid="WRONG_UID",
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=products["table"],
        )

        assert response.status_code == 404
