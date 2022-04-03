def list_all_selector(*, table):
    return table.scan()["Items"]
