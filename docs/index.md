```{include} ../README.md
:start-line: 0
:end-line: 4
```

_For background, see [Lamin Blog #5 (2022)](https://lamin.ai/notes/2022/nbproject)._

Track & reproduce notebooks through metadata like version, time stamps, dependencies, and integrity status.

Monitor data flow in and out of notebooks by integrating with a data platform like [LaminDB](https://lamin.ai/lamindb).

Supported editors:

- Jupyter Lab (best experience)
- VS Code & Jupyter Notebook (no interactive experience, some quirks)

Install:

```
pip install nbproject
```

Get started:

```
from nbproject import header
```

→ This will initialize nbproject, display notebook metadata, and start tracking! Done.

Documentation:

- Learn usage patterns in the [tutorials](tutorials/index).
- Check out the [API reference](api).
- If you get stuck, see our [guides](guides/index) for edge cases & errors.

```{toctree}
:maxdepth: 1
:hidden:

tutorials/index
api
guides/index
changelog
```
