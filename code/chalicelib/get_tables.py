from chalicelib.utils.table_getter import TableGetter

get_products_table = TableGetter(env_name="PRODUCTS_TABLE_NAME")
get_users_table = TableGetter(env_name="USERS_TABLE_NAME")
get_carts_table = TableGetter(env_name="CARTS_TABLE_NAME")
get_orders_table = TableGetter(env_name="ORDERS_TABLE_NAME")
