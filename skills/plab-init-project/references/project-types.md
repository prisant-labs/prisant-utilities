# Project Types

Project types add language/domain-specific files and .gitignore entries on top of the profile structure. Select with the `--type` flag (default: `general`).

## general (default)

No additional files or directories. The profile structure is used as-is.

## code-python

Adds the following to the project root:

```
src/
  __init__.py
tests/
  __init__.py
pyproject.toml
.python-version
```

Appends to .gitignore:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.eggs/
.venv/
venv/
dist/
build/
*.egg
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

## code-node

Adds the following to the project root:

```
src/
package.json
.nvmrc
```

Appends to .gitignore:
```
# Node
node_modules/
dist/
build/
*.tsbuildinfo
.env.local
.env.development.local
.env.test.local
.env.production.local
coverage/
```

## Adding New Types

To add a new project type, add a section to this file with:
1. The directory/file tree it creates
2. The .gitignore entries it appends

The SKILL.md workflow references this file - no changes to SKILL.md are needed when adding types.
