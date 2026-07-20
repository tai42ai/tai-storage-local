"""Local-filesystem ``Storage`` backend for the TAI ecosystem.

Importing this package registers :class:`~tai_storage_local.storage.LocalStorage`
as the active storage provider (the ``@register_storage`` decorator fires as an
import side-effect). A manifest activates the backend by naming this package in
its ``storage_module`` field.
"""

from __future__ import annotations

from tai_storage_local.driver import AsyncLocalDriver
from tai_storage_local.settings import LocalStorageSettings, storage_settings
from tai_storage_local.storage import LocalStorage

__all__ = [
    "AsyncLocalDriver",
    "LocalStorage",
    "LocalStorageSettings",
    "storage_settings",
]
