import pytest
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from httpx import AsyncClient
from loguru import logger

from modules.orders.orders_schemas import OrdersCreate, OrdersInDB, OrdersToUpdate


pytestmark = pytest.mark.asyncio
#Con esta linea anterior podemos eliminar el comando @pytest.mark.asyncio de cada una de las pruebas,
#ya que pytest sabe que todas las pruebas de este archivo son asincronas.


class TestOrdersRoutes:
    # @pytest.mark.asyncio
    async def test_create_orders_route_exists(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("orders:create-orders"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        
        
#Prueba de creacion del inventario:
class TestCreateOrders:
    # @pytest.mark.asyncio
    async def test_valid_input_creates_orders(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res = await client.post(
            app.url_path_for("orders:create-orders"),
            json={"orders": {"orders_name":"test_orders", "state":"test_state"}},
        )
        
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert data["id"] != None
        assert data["orders_name"] == "test_orders"
        
            
    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("orders_name", None, 422),
            ("orders_name", "", 422),
            ("orders_name", "ab", 422),
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
        new_orders = {
            "orders_name": ""
        }
        new_orders[attr] = value
        res = await client.post(
            app.url_path_for("orders:create-orders"),
            json={"orders": new_orders}
        )
        
        assert res.status_code == status_code
    
    
    
        
class TestGetOrders:
    #Obtener una lista de tareas:
    async def test_get_orders_list(
        self,app: FastAPI, authorized_client: AsyncClient
    ) -> None:
        client = await authorized_client
        
        res = await client.get(app.url_path_for("orders:orders_list"))
        
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) > 0
        
        
        
    #Obtener una tarea por su id:
    async def test_get_orders_by_id(
        self, 
        app: FastAPI, 
        authorized_client: AsyncClient, 
    ) -> None:
        client = await authorized_client

        # se crea una tarea de prueba para obtener el id de DB        
        test_orders = {
            "orders_name": "Otra test orders",
            "state":"test_state"
        }

        res1 = await client.post(
            app.url_path_for("orders:create-orders"), json={"orders": test_orders}
        )
        test_data = res1.json()
        print(test_data)
        test_id = str(test_data["id"]) #Error-------------------

        # aqui comienza la verdadera prueba
        res = await client.get(
            app.url_path_for("orders:get-orders-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK
        orders = OrdersInDB(**res.json())

        assert str(orders.id) == test_id
        assert orders.orders_name == test_data["orders_name"]
        
        
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

        res = await client.get(app.url_path_for("orders:get-orders-by-id", id=id))

        assert res.status_code == status_code



class TestUpdateOrders:
    async def test_update_orders_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient, 
        
    ) -> None:
        client = await authorized_client

        res1 = await client.get(
            app.url_path_for("orders:orders_list")
        )
        orders_in_db = res1.json().get("data")[0]

        test_id = orders_in_db.get("id")

        orders_update = OrdersToUpdate(
            orders_name = "Nombre de prueba cambiado",
            state = "test_state"
        )

        res = await client.put(
            app.url_path_for("orders:update-orders-by-id", id=test_id), json={"orders_update": orders_update.dict()}
        )
        assert res.status_code == status.HTTP_200_OK
        orders_updated = res.json()
        assert orders_updated["orders_name"] == orders_update.orders_name

    @pytest.mark.parametrize(
        "attrs_to_change, value",
        (
            ("is_active", False),
            ("is_active", True),
        ),
    )
    async def test_deactivate_activate_orders_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        attrs_to_change: str,
        value: bool,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.get(
            app.url_path_for("orders:orders_list")
        )
        orders_in_db = res1.json().get("data")[0]
        test_id = orders_in_db.get("id")

        orders_update = {"orders_update": {attrs_to_change: value}}
        res = await client.put(
            app.url_path_for("orders:update-orders-by-id", id=test_id), json={"orders_update": orders_update}
        )
        assert res.status_code == status.HTTP_200_OK
        
        
        
        
        
        
class TestDeleteOrders:
    async def test_can_delete_orders(self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.post(
            app.url_path_for("orders:create-orders"), json={"orders": {"orders_name": "inventario para borrar", "state":"test_state"}}
        )
        orders_in_db = res1.json()

        test_id = orders_in_db.get("id")

        res = await client.delete(
            app.url_path_for("orders:delete-orders-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK

# def test_placeholder():
#     pass
