from typing import List

from loguru import logger


async def get_permissions() -> List:
    """_
        function that configurates and returns permissions to access
        all routes defined in the system

    Returns:
        a List[Dict[key: "funtionality_name" : route[List[Dict]]]]
        List: _description_
    """

    permissions = [
        {
            "functionality": "USUARIOS",
            "routes": [
                {"permissions:list-permissions": "Listar permisos"},
                {"roles:create-role": "Crear rol"},
                {"roles:roles_list": "Listar roles"},
                {"roles:get-role-by-id": "Obtener un rol por su id"},
                {"roles:update-role-by-id": "Actualizar un rol por su id"},
                {"roles:update-activate-role-by-id": "Activar / Desactivar un rol por su id"},
                {"roles:delete-role-by-id": "Eliminar un rol por su id"},
                {"users:create-user": "Crear usuario"},
                {"users:users_list": "Listar usuarios"},
                {"users:get-user-by-id": "Obtener un usuario por su id"},
                {"users:activate-user-by-id": "Activar / Desactivar un usuario por su id"},
                {"users:update-user-by-id": "Actualizar un usuario por su id"},
                {"users:delete-user-by-id": "Eliminar un usuario por su id"},
                {"users:change-password-by-id": "Actualizar password por el propio usuario"},
            ],
        },
        {
            "functionality": "INVENTARIO",
            "routes": [
                {"inventory:create-inventory": "Crear inventario"},
                {"inventory:get_inventory_list": "Listar inventario"},
                {"inventory:get-inventory-by-id": "Obtener una inventario por su ID"},
                {"inventory:update-inventory-by-id": "Actualizar una inventario por su ID"},
                {"inventory:delete-inventory-by-id": "Eliminar una inventario por su ID"}
            ]
        },
        {
            "functionality": "RAW_MATERIAL",
            "routes": [
                {"raw_material:create-raw_material": "Crear materia prima"},
                {"raw_material:get_raw_material_list": "Listar materia prima"},
                {"raw_material:get-raw_material-by-id": "Obtener una materia prima por su ID"},
                {"raw_material:update-raw_material-by-id": "Actualizar una materia prima por su ID"},
                {"raw_material:delete-raw_material-by-id": "Eliminar una materia prima por su ID"}
            ]
        },
        {
            "functionality": "PRODUCT",
            "routes": [
                {"product:create-product": "Crear producto"},
                {"product:get_product_list": "Listar producto"},
                {"product:get-product-by-id": "Obtener producto por su ID"},
                {"product:update-product-by-id": "Actualizar producto por su ID"},
                {"product:delete-product-by-id": "Eliminar producto por su ID"}
            ]
        },
        {
            "functionality": "ORDERS",
            "routes": [
                {"orders:create-orders": "Crear pedido"},
                {"orders:get_orders_list": "Listar pedidos"},
                {"orders:get-orders-by-id": "Obtener pedido por su ID"},
                {"orders:update-orders-by-id": "Actualizar pedido por su ID"},
                {"orders:delete-orders-by-id": "Eliminar pedido por su ID"}
            ]
        },
                
    ]

    return permissions


async def verify_permissions(permission: str) -> bool:
    permissions = await get_permissions()

    found = False
    for dic in permissions:
        routes = dic.get("routes")
        for route in routes:
            if permission in route:
                found = True
                return found

    return found
