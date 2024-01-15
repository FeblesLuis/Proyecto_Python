from typing import Any
from shared.utils.app_exceptions import AppExceptionCase


class OrdersExceptions:
    class OrdersCreateException(AppExceptionCase):
        """
        Orders create failed
        """
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el inventario"
            AppExceptionCase.__init__(self, status_code, msg)
    
    class OrdersNotFoundException(AppExceptionCase):
        """
        Orders's ID not found
        """
        
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la BD"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class OrdersIdNoValidException(AppExceptionCase):
        """_
        Orders Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de tarea inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class OrdersInvalidUpdateParamsException(AppExceptionCase):
        """_
        Orders Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)