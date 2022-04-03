def get_item_by_username(table, username):
    return table.get_item(Key={"username": username}).get("Item")
