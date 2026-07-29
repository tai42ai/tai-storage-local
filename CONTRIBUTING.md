# Contributing to tai42-storage-local

`tai42-storage-local` is the local-filesystem **Storage** backend for the TAI
ecosystem: it implements `tai42_contract.storage.Storage` over a directory tree on
the local disk, serving both text and binary content. The hard rule (the plugin
rule): **it depends on `tai42-contract` + `tai42-kit` only and never imports the
skeleton.** Importing the `tai42_storage_local` package fires the
`@tai42_app.storage.register_storage` decorator on `LocalStorage` as a side-effect,
so naming the package in a manifest's `storage_module` activates it — there is no
import edge to the skeleton in either direction.

## Ground rules

- **No skeleton import — ever.** The package is contract-facing; the ban is
  enforced by ruff (`flake8-tidy-imports`), so a stray import fails lint:
  ```bash
  grep -rn "tai42_skeleton" src/   # must be empty
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

## Naming

PyPI is a flat namespace with no owner in the path, so distributions carry the
`tai42-` prefix. GitHub repositories keep their `tai-` names, because the
`tai42ai` organisation already namespaces them. Import packages follow the
distribution.

| Surface | Form |
| --- | --- |
| Distribution — PyPI, `pip install`, dependency pins | `tai42-<name>` |
| Import package | `tai42_<name>` |
| GitHub repository | `tai-<name>` |

So a dependency is declared as `tai42-<name>` while its repository is named
`tai-<name>`, and both spellings are correct in their own context.

Some surfaces are deliberately neither, and must not be renamed: the `tai` CLI
command (`tai42` is an alias), the Prometheus metric namespace (`tai_tool_*`),
`TAI_*` environment variables, and the `tai-plugin.yml` descriptor filename.

## Dev

```bash
uv venv --python 3.13
uv pip install --no-sources --group dev --editable .
uv run --no-sync pytest --cov --cov-report=term-missing
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright
```

`make dev` installs the sibling `tai-contract` and `tai-kit` repos as editable installs for local cross-repo development.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
