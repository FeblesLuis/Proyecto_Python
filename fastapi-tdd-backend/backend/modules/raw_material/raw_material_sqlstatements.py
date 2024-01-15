CREATE_RAW_MATERIAL_ITEM = """
    INSERT INTO raw_material (id, raw_material_name, type, provider, quantity, adquisition_date, is_active, created_by, created_at, updated_by, updated_at)
    VALUES (:id, :raw_material_name, :type, :provider, :quantity, :adquisition_date, :is_active,  :created_by, :created_at, :updated_by, :updated_at)
    RETURNING id, raw_material_name, type, provider, quantity, adquisition_date, is_active, created_by, created_at, updated_by, updated_at;
"""

GET_RAW_MATERIAL_LIST = """
    SELECT t.id, t.raw_material_name, t.type, t.provider, t.quantity, t.adquisition_date, t.is_active, t.created_at, t.updated_at, 
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM raw_material AS t
    LEFT JOIN users AS us1 ON us1.id = t.created_by
    LEFT JOIN users AS us2 ON us2.id = t.updated_by
"""


def raw_material_list_search():
    return """ WHERE (t.raw_material_name LIKE :search) """

def raw_material_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY t.raw_material_name ASC;"
    elif order == "raw_material_name" and direction == "DESC":
        sql_sentence = " ORDER BY t.raw_material_name DESC;"
    elif order == "raw_material_name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.raw_material_name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY t.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY t.is_active ASC;"

    return sql_sentence


GET_RAW_MATERIAL_BY_ID = """
    SELECT t.id, t.raw_material_name, t.type, t.provider, t.quantity, t.adquisition_date, t.is_active, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM raw_material AS t
    WHERE t.id = :id; 
"""

UPDATE_RAW_MATERIAL_BY_ID = """
    UPDATE raw_material
    SET raw_material_name = :raw_material_name,
        type           = :type,
        provider       = :provider,
        quantity       = :quantity,
        adquisition_date = :adquisition_date,
        is_active      = :is_active,
        created_by     = :created_by,
        created_at     = :created_at,
        updated_by     = :updated_by,
        updated_at     = :updated_at
    WHERE id = :id
    RETURNING id, raw_material_name, type, provider, quantity, adquisition_date, is_active, created_by, created_at, updated_by, updated_at;
"""

DELETE_RAW_MATERIAL_BY_ID = """
    DELETE FROM raw_material
    WHERE id = :id
    RETURNING id;
"""