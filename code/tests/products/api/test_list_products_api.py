class TestListProductsAPI:
    @staticmethod
    def run_test(
        *,
        token,
        client,
        mocker,
        table,
        product,
        path: str = "/products",
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

        return client.http.get(path=path, headers=headers, body=None)

    def test_list_products(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_1"]["product_0"]
        products_table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            mocker=mocker,
            product=product,
            table=products_table,
        )

        assert len(response.json_body) == 5
        assert response.status_code == 200

    def test_query_param_next(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_3"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            mocker=mocker,
            product=product,
            table=table,
        )

        next_uid = response.json_body[-1]["uid"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            path=f"/products?next={next_uid}",
            mocker=mocker,
            product=product,
            table=table,
        )

        assert len(response.json_body) == 2
        assert response.status_code == 200

    def test_query_param_back(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_1"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            mocker=mocker,
            product=product,
            table=table,
        )

        back_uid = response.json_body[-1]["uid"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            path=f"/products?back={back_uid}",
            mocker=mocker,
            product=product,
            table=table,
        )

        assert len(response.json_body) == 4
        assert response.status_code == 200

    def test_list_products_of_user(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_2"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            path="/products/of-user/username_2",
            mocker=mocker,
            product=product,
            table=table,
        )

        assert len(response.json_body) == 3
        assert response.status_code == 200

    def test_query_param_next_for_certain_user(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_2"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            mocker=mocker,
            product=product,
            table=table,
        )

        next_uid = response.json_body[0]["uid"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            path=f"/products/of-user/username_2?next={next_uid}",
            mocker=mocker,
            product=product,
            table=table,
        )

        assert len(response.json_body) == 2
        assert response.status_code == 200

    def test_query_param_back_for_certain_user(
        self, authorized_user_token, client, mocker, products
    ):
        product = products["products_of_user_2"]["product_0"]
        table = products["table"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            mocker=mocker,
            product=product,
            table=table,
        )

        back_uid = response.json_body[-1]["uid"]
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            path=f"/products/of-user/username_2?back={back_uid}",
            mocker=mocker,
            product=product,
            table=table,
        )

        assert len(response.json_body) == 2
        assert response.status_code == 200
