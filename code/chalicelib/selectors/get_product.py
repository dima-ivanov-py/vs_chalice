def get_product_selector(*, table, uid: str, username: str):
    return table.get_item(Key={"username": username, "uid": uid})["Item"]
