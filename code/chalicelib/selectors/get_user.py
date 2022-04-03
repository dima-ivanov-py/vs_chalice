def get_user_selector(table, username):
    return table.get_item(Key={"username": username})["Item"]
