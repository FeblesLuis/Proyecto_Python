from typing import Any
from shared.utils.app_exceptions import AppExceptionCase


class Raw_materialExceptions:
    class Raw_materialCreateException(AppExceptionCase):
        """
        Raw_material create failed
        """
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando la materia prima"
            AppExceptionCase.__init__(self, status_code, msg)
    
    class Raw_materialNotFoundException(AppExceptionCase):
        """
        Raw_material's ID not found
        """
        
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la BD"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class Raw_materialIdNoValidException(AppExceptionCase):
        """_
        Raw_material Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de tarea inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class Raw_materialInvalidUpdateParamsException(AppExceptionCase):
        """_
        Raw_material Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)