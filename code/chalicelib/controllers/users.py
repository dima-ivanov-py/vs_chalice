from chalicelib.get_tables import get_users_table
from chalicelib.selectors.list_all import list_all_selector


def list_users_all_response(request):
    table = get_users_table()
    result = list_all_selector(table=table)
    return {obj["username"]: obj["status"] for obj in result}
