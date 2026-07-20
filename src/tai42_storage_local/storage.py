"""The local-filesystem :class:`~tai42_contract.storage.Storage` backend.

``LocalStorage`` implements the full storage contract — the five text methods plus
the binary ``load_bytes`` / ``upload_bytes`` — over a directory tree on the local
disk. It owns no pooled client (the local filesystem needs none): each call builds
a stateless :class:`~tai42_storage_local.driver.AsyncLocalDriver` from the cached
settings, so a live-reload of the env-driven root path takes effect on the next
call. ``stat`` inherits the contract's ``mimetypes``-based path inference (the
local filesystem stores no content-type metadata).

Registering the class fires ``@tai42_app.storage.register_storage`` as an import
side-effect, so a manifest names this package via ``storage_module`` to activate
the backend.
"""

from __future__ import annotations

import logging

from tai42_contract.app import tai42_app
from tai42_contract.storage import Storage, assert_not_root

from tai42_storage_local.driver import AsyncLocalDriver
from tai42_storage_local.settings import storage_settings

logger = logging.getLogger(__name__)


# Importing this module registers LocalStorage as the active storage provider (a
# manifest's storage_module field names this package to import; there is no
# entry-point). The decorator returns the class unchanged.
@tai42_app.storage.register_storage
class LocalStorage(Storage):
    def _driver(self) -> AsyncLocalDriver:
        settings = storage_settings()
        return AsyncLocalDriver(root_path=settings.root_path, create_dirs=settings.create_dirs)

    async def load(self, path: str) -> str:
        try:
            return await self._driver().read_file(path)
        except FileNotFoundError as e:
            # Re-raise with the relative path, not the raw OS message (which
            # leaks the absolute root).
            raise FileNotFoundError(f"Object not found: {path}") from e

    async def list(self) -> list[str]:
        return await self._driver().list_recursive()

    async def upload(self, path: str, content: str) -> None:
        await self._driver().write_file(path, content)
        logger.info("Wrote object to local storage: %s", path)

    async def delete(self, path: str) -> None:
        try:
            await self._driver().delete_file(path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Object not found: {path}") from e
        logger.info("Deleted object from local storage: %s", path)

    async def delete_dir(self, path: str) -> None:
        assert_not_root(path)
        await self._driver().delete_dir(path)
        logger.info("Deleted directory from local storage: %s", path)

    async def load_bytes(self, path: str) -> bytes:
        try:
            return await self._driver().read_bytes(path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Object not found: {path}") from e

    async def upload_bytes(self, path: str, data: bytes, content_type: str | None = None) -> None:
        # The local filesystem keeps no MIME metadata, so ``content_type`` is
        # accepted for contract parity but not stored; ``stat`` re-infers it from
        # the path suffix.
        await self._driver().write_bytes(path, data)
        logger.info("Wrote bytes to local storage: %s", path)
