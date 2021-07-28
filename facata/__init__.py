from facata.core import connect
from facata.exceptions import FacataException

__all__ = ["FacataException", "connect"]

from . import _version

__version__ = _version.get_versions()["version"]
