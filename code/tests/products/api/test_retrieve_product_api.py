class TestRetrieveProductAPI:
    @staticmethod
    def run_test(
        *,
        token,
        client,
        product,
        mocker,
        table,
        path: str = "/products",
        uid: str,
        headers=None,
    ):
        mocker.patch(
            "chalicelib.controllers.products.get_products_table",
            return_value=table,
        )

        mocker.patch(
            "chalicelib.controllers.products.get_authorized_username",
            return_value=product["username"],
        )

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Authorization": token,
            }

        return client.http.get(path=f"{path}/{uid}", headers=headers)

    def test_can_retrieve_product(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_1"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            product=product,
            mocker=mocker,
            table=table,
            uid=product["uid"],
        )

        assert response.status_code == 200

    def test_wrong_uid(self, authorized_user_token, client, mocker, products):
        product = products["products_of_user_1"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            product=product,
            mocker=mocker,
            table=table,
            uid="WRONG_UID",
        )

        assert response.status_code == 404
