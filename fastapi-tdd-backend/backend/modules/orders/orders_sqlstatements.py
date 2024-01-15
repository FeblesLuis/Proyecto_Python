CREATE_ORDERS_ITEM = """
    INSERT INTO orders (id, orders_name, state, is_active, created_by, created_at, updated_by, updated_at)
    VALUES (:id, :orders_name, :state, :is_active,  :created_by, :created_at, :updated_by, :updated_at)
    RETURNING id, orders_name, state, is_active, created_by, created_at, updated_by, updated_at;
"""

GET_ORDERS_LIST = """
    SELECT t.id, t.orders_name, t.state, t.is_active, t.created_at, t.updated_at, 
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM orders AS t
    LEFT JOIN users AS us1 ON us1.id = t.created_by
    LEFT JOIN users AS us2 ON us2.id = t.updated_by
"""


def orders_list_search():
    return """ WHERE (t.orders_name LIKE :search) """

def orders_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY t.orders_name ASC;"
    elif order == "orders_name" and direction == "DESC":
        sql_sentence = " ORDER BY t.orders_name DESC;"
    elif order == "orders_name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.orders_name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY t.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.is_active ASC;"

    return sql_sentence


GET_ORDERS_BY_ID = """
    SELECT t.id, t.orders_name, t.state, t.is_active, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM orders AS t
    WHERE t.id = :id; 
"""

UPDATE_ORDERS_BY_ID = """
    UPDATE orders
    SET orders_name = :orders_name,
        state          = :state,
        is_active      = :is_active,
        created_by     = :created_by,
        created_at     = :created_at,
        updated_by     = :updated_by,
        updated_at     = :updated_at
    WHERE id = :id
    RETURNING id, orders_name, state, is_active, created_by, created_at, updated_by, updated_at;
"""

DELETE_ORDERS_BY_ID = """
    DELETE FROM orders
    WHERE id = :id
    RETURNING id;
"""