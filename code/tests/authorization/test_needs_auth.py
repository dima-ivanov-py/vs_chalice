import os


def test_needs_auth(client):
    headers_1 = {
        "Content-Type": "application/json",
        "Authorization": os.getenv("TK"),
    }

    headers_2 = {
        "Content-Type": "application/json",
        "Authorization": "WRONG_TOKEN",
    }

    assert client.http.get("/products", headers=headers_1).status_code == 200
    assert client.http.get("/products", headers=headers_2).status_code == 403
