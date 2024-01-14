CREATE_INVENTORY_ITEM = """
    INSERT INTO inventory (id, inventory_name, location_stock, is_active, created_by, created_at, updated_by, updated_at)
    VALUES (:id, :inventory_name, :location_stock, :is_active,  :created_by, :created_at, :updated_by, :updated_at)
    RETURNING id, inventory_name, location_stock, is_active, created_by, created_at, updated_by, updated_at;
"""

GET_INVENTORY_LIST = """
    SELECT t.id, t.inventory_name, t.location_stock, t.is_active, t.created_at, t.updated_at, 
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM inventory AS t
    LEFT JOIN users AS us1 ON us1.id = t.created_by
    LEFT JOIN users AS us2 ON us2.id = t.updated_by
"""


def inventory_list_search():
    return """ WHERE (t.inventory_name LIKE :search) """

def inventory_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY t.inventory_name ASC;"
    elif order == "inventory_name" and direction == "DESC":
        sql_sentence = " ORDER BY t.inventory_name DESC;"
    elif order == "inventory_name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.inventory_name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY t.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.is_active ASC;"

    return sql_sentence


GET_INVENTORY_BY_ID = """
    SELECT t.id, t.inventory_name, t.location_stock, t.is_active, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM inventory AS t
    WHERE t.id = :id; 
"""

UPDATE_INVENTORY_BY_ID = """
    UPDATE inventory
    SET inventory_name = :inventory_name,
        location_stock = :location_stock,
        is_active      = :is_active,
        created_by     = :created_by,
        created_at     = :created_at,
        updated_by     = :updated_by,
        updated_at     = :updated_at
    WHERE id = :id
    RETURNING id, inventory_name, location_stock, is_active, created_by, created_at, updated_by, updated_at;
"""

DELETE_INVENTORY_BY_ID = """
    DELETE FROM inventory
    WHERE id = :id
    RETURNING id;
"""