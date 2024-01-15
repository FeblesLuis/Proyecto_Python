import pytest
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from httpx import AsyncClient
from loguru import logger

from modules.raw_material.raw_material_schemas import Raw_materialCreate, Raw_materialInDB, Raw_materialToUpdate


pytestmark = pytest.mark.asyncio
#Con esta linea anterior podemos eliminar el comando @pytest.mark.asyncio de cada una de las pruebas,
#ya que pytest sabe que todas las pruebas de este archivo son asincronas.


class TestRaw_materialRoutes:
    # @pytest.mark.asyncio
    async def test_create_raw_material_route_exists(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("raw_material:create-raw_material"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        
        
#Prueba de creacion de la materia prima:
class TestCreateRaw_material:
    # @pytest.mark.asyncio
    async def test_valid_input_creates_raw_material(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res = await client.post(
            app.url_path_for("raw_material:create-raw_material"),
            json={"raw_material": {"raw_material_name":"test_raw_material", "provider":"test_provider", "quantity": 10}},
        )
        
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert data["id"] != None
        assert data["raw_material_name"] == "test_raw_material"
        
            
    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("raw_material_name", None, 422),
            ("raw_material_name", "", 422),
            ("raw_material_name", "ab", 422),
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
        new_raw_material = {
            "raw_material_name": ""
        }
        new_raw_material[attr] = value
        res = await client.post(
            app.url_path_for("raw_material:create-raw_material"),
            json={"raw_material": new_raw_material}
        )
        
        assert res.status_code == status_code
    
    
    
        
class TestGetRaw_material:
    #Obtener una lista de materias primas:
    async def test_get_raw_material_list(
        self,app: FastAPI, authorized_client: AsyncClient
    ) -> None:
        client = await authorized_client
        
        res = await client.get(app.url_path_for("raw_material:raw_material_list"))
        
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) > 0
        
        
        
    #Obtener una materia prima por su id:
    async def test_get_raw_material_by_id(
        self, 
        app: FastAPI, 
        authorized_client: AsyncClient, 
    ) -> None:
        client = await authorized_client

        # se crea una materia prima de prueba para obtener el id de DB        
        test_raw_material = {
            "raw_material_name": "Otra test raw_material",
            "provider": "Otra test of provider",
            "quantity": 10
        }

        res1 = await client.post(
            app.url_path_for("raw_material:create-raw_material"), json={"raw_material": test_raw_material}
        )
        test_data = res1.json()
        print(test_data)
        test_id = str(test_data["id"]) #E

        # aqui comienza la verdadera prueba
        res = await client.get(
            app.url_path_for("raw_material:get-raw_material-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK
        raw_material = Raw_materialInDB(**res.json())

        assert str(raw_material.id) == test_id
        assert raw_material.raw_material_name == test_data["raw_material_name"]
        
        
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

        res = await client.get(app.url_path_for("raw_material:get-raw_material-by-id", id=id))

        assert res.status_code == status_code



class TestUpdateRaw_material:
    async def test_update_raw_material_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient, 
        
    ) -> None:
        client = await authorized_client

        res1 = await client.get(
            app.url_path_for("raw_material:raw_material_list")
        )
        raw_material_in_db = res1.json().get("data")[0]

        test_id = raw_material_in_db.get("id")

        raw_material_update = Raw_materialToUpdate(
            raw_material_name = "Nombre de prueba cambiado",
            provider = "proveedor de prueba cambiada",
            quantity = 15
        )

        res = await client.put(
            app.url_path_for("raw_material:update-raw_material-by-id", id=test_id), json={"raw_material_update": raw_material_update.dict()}
        )
        assert res.status_code == status.HTTP_200_OK
        raw_material_updated = res.json()
        assert raw_material_updated["raw_material_name"] == raw_material_update.raw_material_name

    @pytest.mark.parametrize(
        "attrs_to_change, value",
        (
            ("is_active", False),
            ("is_active", True),
        ),
    )
    async def test_deactivate_activate_raw_material_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        attrs_to_change: str,
        value: bool,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.get(
            app.url_path_for("raw_material:raw_material_list")
        )
        raw_material_in_db = res1.json().get("data")[0]
        test_id = raw_material_in_db.get("id")

        raw_material_update = {"raw_material_update": {attrs_to_change: value}}
        res = await client.put(
            app.url_path_for("raw_material:update-raw_material-by-id", id=test_id), json={"raw_material_update": raw_material_update}
        )
        assert res.status_code == status.HTTP_200_OK
        
        
        
        
        
        
class TestDeleteRaw_material:
    async def test_can_delete_raw_material(self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.post(
            app.url_path_for("raw_material:create-raw_material"), json={"raw_material": {"raw_material_name": "inventario para borrar", "provider": "proveedor para borrar", "quantity": 20}}
        )
        raw_material_in_db = res1.json()

        test_id = raw_material_in_db.get("id")

        res = await client.delete(
            app.url_path_for("raw_material:delete-raw_material-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK

# def test_placeholder():
#     pass
