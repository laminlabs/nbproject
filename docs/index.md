```{include} ../README.md
:start-line: 0
:end-line: 4
```

Manage reproducible notebooks with metadata, dependency, and integrity tracking.
Share notebooks your collaborators can trust.

Supported editors:

- Jupyter Lab (interactive experience)
- VS Code & Jupyter Notebook (no interactive experience)

Install:

```
pip install nbproject
```

Get started:

```
from nbproject import header; header()
```

→ This will initialize nbproject, display notebook metadata, and start tracking! Done. 😅

Documentation:

- {doc}`nutshell`.
- Learn usage in the [tutorials](tutorials/index).
- See the [API reference](api).
- If you get stuck, see [guides](guides/index) for edge cases & errors.

```{toctree}
:maxdepth: 1
:hidden:

tutorials/index
api
guides/index
changelog
```
