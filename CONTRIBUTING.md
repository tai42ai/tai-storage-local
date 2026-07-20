# Contributing to tai-storage-local

`tai-storage-local` is the local-filesystem **Storage** backend for the TAI
ecosystem: it implements `tai_contract.storage.Storage` over a directory tree on
the local disk, serving both text and binary content. The hard rule (the plugin
rule): **it depends on `tai-contract` + `tai-kit` only and never imports the
skeleton.** Importing the `tai_storage_local` package fires the
`@tai_app.storage.register_storage` decorator on `LocalStorage` as a side-effect,
so naming the package in a manifest's `storage_module` activates it — there is no
import edge to the skeleton in either direction.

## Ground rules

- **No skeleton import — ever.** The package is contract-facing; the ban is
  enforced by ruff (`flake8-tidy-imports`), so a stray import fails lint:
  ```bash
  grep -rn "tai_skeleton" src/   # must be empty
  ```
- **Every path stays under the root.** A stored path is resolved under the
  configured root and rejected if it escapes it (a path-boundary check, not a
  string prefix); `delete_dir` refuses the storage root itself.
- **Loud errors.** No swallowed exceptions, silent fallbacks, or silent
  truncation. A missing file raises `FileNotFoundError`; a boundary violation
  raises.
- **Typed package** (`py.typed`). Pyright runs clean.

## Layout

- `storage.py` — `LocalStorage` (the `Storage` impl) and its registration.
- `driver.py` — the filesystem read/write driver and the path-boundary guard.
- `settings.py` — the `STORAGE_LOCAL_` settings.

## Dev

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

For local cross-repo work, `make dev` editable-installs the sibling `tai-*`
checkouts this package builds on into the venv. While `[tool.uv.sources]` pins
those siblings to local paths, `uv sync` already installs them editable and
`make dev` changes nothing; once the lock resolves them from the registry,
`uv sync` / `uv run` installs the published builds instead, so re-run
`make dev` afterward to restore the editable links.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
