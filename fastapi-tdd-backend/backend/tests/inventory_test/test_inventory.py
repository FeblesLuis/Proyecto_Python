import pytest
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from httpx import AsyncClient
from loguru import logger

from modules.inventory.inventory_schemas import InventoryCreate, InventoryInDB, InventoryToUpdate


pytestmark = pytest.mark.asyncio
#Con esta linea anterior podemos eliminar el comando @pytest.mark.asyncio de cada una de las pruebas,
#ya que pytest sabe que todas las pruebas de este archivo son asincronas.


class TestInventoryRoutes:
    # @pytest.mark.asyncio
    async def test_create_inventory_route_exists(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("inventory:create-inventory"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        
        
#Prueba de creacion del inventario:
class TestCreateInventory:
    # @pytest.mark.asyncio
    async def test_valid_input_creates_inventory(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res = await client.post(
            app.url_path_for("inventory:create-inventory"),
            json={"inventory": {"inventory_name":"test_inventory", "location_stock":"test_location"}},
        )
        
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert data["id"] != None
        assert data["inventory_name"] == "test_inventory"
        
            
    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("inventory_name", None, 422),
            ("inventory_name", "", 422),
            ("inventory_name", "ab", 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        attr: str,
        value: str,
        status_code: int,
    ) -> None:
        client = await authorized_client
        new_inventory = {
            "inventory_name": ""
        }
        new_inventory[attr] = value
        res = await client.post(
            app.url_path_for("inventory:create-inventory"),
            json={"inventory": new_inventory}
        )
        
        assert res.status_code == status_code
    
    
    
        
class TestGetInventory:
    #Obtener una lista de tareas:
    async def test_get_inventory_list(
        self,app: FastAPI, authorized_client: AsyncClient
    ) -> None:
        client = await authorized_client
        
        res = await client.get(app.url_path_for("inventory:inventory_list"))
        
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) > 0
        
        
        
    #Obtener una tarea por su id:
    async def test_get_inventory_by_id(
        self, 
        app: FastAPI, 
        authorized_client: AsyncClient, 
    ) -> None:
        client = await authorized_client

        # se crea una tarea de prueba para obtener el id de DB        
        test_inventory = {
            "inventory_name": "Otra test inventory",
            "location_stock": "Otra test location"
        }

        res1 = await client.post(
            app.url_path_for("inventory:create-inventory"), json={"inventory": test_inventory}
        )
        test_data = res1.json()
        print(test_data)
        test_id = str(test_data["id"]) #Error-------------------

        # aqui comienza la verdadera prueba
        res = await client.get(
            app.url_path_for("inventory:get-inventory-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK
        inventory = InventoryInDB(**res.json())

        assert str(inventory.id) == test_id
        assert inventory.inventory_name == test_data["inventory_name"]
        
        
    @pytest.mark.parametrize(
        "id, status_code",
        (
            (uuid4(), 404), 
            (None, 422), 
            ("abc123", 422)
        ),
    )
    async def test_wrong_id_returns_error(
        self, 
        app: FastAPI, 
        authorized_client: AsyncClient, 
        id: UUID, 
        status_code: int
    ) -> None:
        client = await authorized_client

        res = await client.get(app.url_path_for("inventory:get-inventory-by-id", id=id))

        assert res.status_code == status_code



class TestUpdateInventory:
    async def test_update_inventory_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient, 
        
    ) -> None:
        client = await authorized_client

        res1 = await client.get(
            app.url_path_for("inventory:inventory_list")
        )
        inventory_in_db = res1.json().get("data")[0]

        test_id = inventory_in_db.get("id")

        inventory_update = InventoryToUpdate(
            inventory_name = "Nombre de prueba cambiado",
            location_stock = "Ubicacion de prueba cambiada"
        )

        res = await client.put(
            app.url_path_for("inventory:update-inventory-by-id", id=test_id), json={"inventory_update": inventory_update.dict()}
        )
        assert res.status_code == status.HTTP_200_OK
        inventory_updated = res.json()
        assert inventory_updated["inventory_name"] == inventory_update.inventory_name

    @pytest.mark.parametrize(
        "attrs_to_change, value",
        (
            ("is_active", False),
            ("is_active", True),
        ),
    )
    async def test_deactivate_activate_inventory_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        attrs_to_change: str,
        value: bool,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.get(
            app.url_path_for("inventory:inventory_list")
        )
        inventory_in_db = res1.json().get("data")[0]
        test_id = inventory_in_db.get("id")

        inventory_update = {"inventory_update": {attrs_to_change: value}}
        res = await client.put(
            app.url_path_for("inventory:update-inventory-by-id", id=test_id), json={"inventory_update": inventory_update}
        )
        assert res.status_code == status.HTTP_200_OK
        
        
        
        
        
        
class TestDeleteInventory:
    async def test_can_delete_inventory(self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.post(
            app.url_path_for("inventory:create-inventory"), json={"inventory": {"inventory_name": "inventario para borrar", "location_stock": "ubicacion para borrar"}}
        )
        inventory_in_db = res1.json()

        test_id = inventory_in_db.get("id")

        res = await client.delete(
            app.url_path_for("inventory:delete-inventory-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK

# def test_placeholder():
#     pass
