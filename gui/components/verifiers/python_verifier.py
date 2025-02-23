import platform

from typing import Tuple

def verify_python() -> Tuple[bool, str]:
    """
    Verifica si Python está instalado y retorna (True, versión) si se puede obtener la versión,
    o (False, "N/A") en caso contrario.
    """
    try:
        version = platform.python_version()
        return True, version
    except Exception:
        return False, "N/A"
