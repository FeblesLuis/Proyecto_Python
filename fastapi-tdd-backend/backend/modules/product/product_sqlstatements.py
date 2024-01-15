CREATE_PRODUCT_ITEM = """
    INSERT INTO product (id, product_name, type, description, price, is_active, created_by, created_at, updated_by, updated_at)
    VALUES (:id, :product_name, :type, :description, :price, :is_active,  :created_by, :created_at, :updated_by, :updated_at)
    RETURNING id, product_name, type, description, price, is_active, created_by, created_at, updated_by, updated_at;
"""

GET_PRODUCT_LIST = """
    SELECT t.id, t.product_name, t.type, t.description, t.price, t.is_active, t.created_at, t.updated_at, 
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM product AS t
    LEFT JOIN users AS us1 ON us1.id = t.created_by
    LEFT JOIN users AS us2 ON us2.id = t.updated_by
"""


def product_list_search():
    return """ WHERE (t.product_name LIKE :search) """

def product_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY t.product_name ASC;"
    elif order == "product_name" and direction == "DESC":
        sql_sentence = " ORDER BY t.product_name DESC;"
    elif order == "product_name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.product_name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY t.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.is_active ASC;"

    return sql_sentence


GET_PRODUCT_BY_ID = """
    SELECT t.id, t.product_name, t.type, t.description, t.price, t.is_active, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM product AS t
    WHERE t.id = :id; 
"""

UPDATE_PRODUCT_BY_ID = """
    UPDATE product
    SET product_name = :product_name,
        type           = :type,
        description    = :description,
        price          = :price,
        is_active      = :is_active,
        created_by     = :created_by,
        created_at     = :created_at,
        updated_by     = :updated_by,
        updated_at     = :updated_at
    WHERE id = :id
    RETURNING id, product_name, type, description, price, is_active, created_by, created_at, updated_by, updated_at;
"""

DELETE_PRODUCT_BY_ID = """
    DELETE FROM product
    WHERE id = :id
    RETURNING id;
"""