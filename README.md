# concierge


# Setup developer environment

To start, you need to setup your local machine.

## Setup venv

You need to setup virtual environment, simplest way is to run from project root directory:

```bash
$ . ./setup_dev_env.sh
```

This will create a new venv, install dependencies and activate the environment.

## Run pre-commit

To reformat and lint all files in the project, use:

```
uv run pre-commit run --all-files
```

The used linters are configured in `.pre-commit-config.yaml`.

# Work with the project

## Manage dependencies

The project uses `uv`, a fast and modern Python package manager that manages dependencies via the `pyproject.toml` file.

### Add dependencies

To add a new package and update the `pyproject.toml` and `uv.lock` files, use:

```bash
uv add <package-name>
```

You can also specify versions, extras, or assign to specific groups:

```bash
uv add requests==2.31.0     # specific version
uv add fastapi[all]         # with extras
uv add --dev pytest         # dev-only dependencies
uv add --group foo uvicorn  # custom group from [dependency-groups]
```

### Remove dependencies

To remove a package and clean up both `pyproject.toml` and `uv.lock` files, use:

```bash
uv remove <package-name>
```

Example:

```bash
uv remove pandas
```

### Lock & install dependencies

Dependency metadata can also be updated manually by editing the `pyproject.toml` file directly.
After making changes, run the following commands to update the `uv.lock` file and install the dependencies:

```bash
uv lock
uv sync
```

You can also sync specific groups:

```bash
uv sync --dev        # development dependencies
uv sync --group foo  # custom dependency group in dependency-groups
```
