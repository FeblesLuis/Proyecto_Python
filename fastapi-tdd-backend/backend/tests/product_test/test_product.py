import pytest
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from httpx import AsyncClient
from loguru import logger

from modules.product.product_schemas import ProductCreate, ProductInDB, ProductToUpdate


pytestmark = pytest.mark.asyncio
#Con esta linea anterior podemos eliminar el comando @pytest.mark.asyncio de cada una de las pruebas,
#ya que pytest sabe que todas las pruebas de este archivo son asincronas.


class TestProductRoutes:
    # @pytest.mark.asyncio
    async def test_create_product_route_exists(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("product:create-product"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        
        
#Prueba de creacion de la materia prima:
class TestCreateProduct:
    # @pytest.mark.asyncio
    async def test_valid_input_creates_product(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res = await client.post(
            app.url_path_for("product:create-product"),
            json={"product": {"product_name":"test_product", "description":"test_description", "price": 10.1}},
        )
        
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert data["id"] != None
        assert data["product_name"] == "test_product"
        
            
    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("product_name", None, 422),
            ("product_name", "", 422),
            ("product_name", "ab", 422),
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
        new_product = {
            "product_name": ""
        }
        new_product[attr] = value
        res = await client.post(
            app.url_path_for("product:create-product"),
            json={"product": new_product}
        )
        
        assert res.status_code == status_code
    
    
    
        
class TestGetProduct:
    #Obtener una lista de materias primas:
    async def test_get_product_list(
        self,app: FastAPI, authorized_client: AsyncClient
    ) -> None:
        client = await authorized_client
        
        res = await client.get(app.url_path_for("product:product_list"))
        
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) > 0
        
        
        
    #Obtener una materia prima por su id:
    async def test_get_product_by_id(
        self, 
        app: FastAPI, 
        authorized_client: AsyncClient, 
    ) -> None:
        client = await authorized_client

        # se crea una materia prima de prueba para obtener el id de DB        
        test_product = {
            "product_name": "Otra test product",
            "description": "Otra test of description",
            "price": 10.1
        }

        res1 = await client.post(
            app.url_path_for("product:create-product"), json={"product": test_product}
        )
        test_data = res1.json()
        print(test_data)
        test_id = str(test_data["id"]) #E

        # aqui comienza la verdadera prueba
        res = await client.get(
            app.url_path_for("product:get-product-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK
        product = ProductInDB(**res.json())

        assert str(product.id) == test_id
        assert product.product_name == test_data["product_name"]
        
        
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

        res = await client.get(app.url_path_for("product:get-product-by-id", id=id))

        assert res.status_code == status_code



class TestUpdateProduct:
    async def test_update_product_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient, 
        
    ) -> None:
        client = await authorized_client

        res1 = await client.get(
            app.url_path_for("product:product_list")
        )
        product_in_db = res1.json().get("data")[0]

        test_id = product_in_db.get("id")

        product_update = ProductToUpdate(
            product_name = "Nombre de prueba cambiado",
            description = "descripción de prueba cambiada",
            price = 15.9
        )

        res = await client.put(
            app.url_path_for("product:update-product-by-id", id=test_id), json={"product_update": product_update.dict()}
        )
        assert res.status_code == status.HTTP_200_OK
        product_updated = res.json()
        assert product_updated["product_name"] == product_update.product_name

    @pytest.mark.parametrize(
        "attrs_to_change, value",
        (
            ("is_active", False),
            ("is_active", True),
        ),
    )
    async def test_deactivate_activate_product_with_valid_data(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        attrs_to_change: str,
        value: bool,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.get(
            app.url_path_for("product:product_list")
        )
        product_in_db = res1.json().get("data")[0]
        test_id = product_in_db.get("id")

        product_update = {"product_update": {attrs_to_change: value}}
        res = await client.put(
            app.url_path_for("product:update-product-by-id", id=test_id), json={"product_update": product_update}
        )
        assert res.status_code == status.HTTP_200_OK
        
        
        
        
        
        
class TestDeleteProduct:
    async def test_can_delete_product(self,
        app: FastAPI,
        authorized_client: AsyncClient,
    ) -> None:
        client = await authorized_client
        
        res1 = await client.post(
            app.url_path_for("product:create-product"), json={"product": {"product_name": "inventario para borrar", "description": "descripcion para borrar", "price": 20.5}}
        )
        product_in_db = res1.json()

        test_id = product_in_db.get("id")

        res = await client.delete(
            app.url_path_for("product:delete-product-by-id", id=test_id)
        )
        assert res.status_code == status.HTTP_200_OK

# def test_placeholder():
#     pass
