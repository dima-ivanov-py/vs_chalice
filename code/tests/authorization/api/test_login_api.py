import json


class TestLoginAPI:
    @staticmethod
    def run_test(
        *,
        table,
        mocker,
        token,
        client,
        data,
        path: str = "/login",
        headers=None,
    ):
        mocker.patch(
            "chalicelib.controllers.login.get_users_table", return_value=table
        )

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Authorization": token,
            }

        return client.http.post(
            path=path, headers=headers, body=json.dumps(data)
        )

    def test_get_jwt_token(self, mocker, client, authorized_user_token):
        table = authorized_user_token["table"]
        data = {
            "username": authorized_user_token["username"],
            "password": authorized_user_token["password"],
        }

        resp = self.run_test(
            mocker=mocker,
            table=table,
            token=authorized_user_token,
            client=client,
            data=data,
        )
        assert type(resp.json_body["token"]) == str
