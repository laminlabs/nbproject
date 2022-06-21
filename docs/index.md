```{include} ../README.md
:start-line: 0
:end-line: 1
```

- Make notebooks reproducible through dependency & integrity tracking.
- Keep track of notebooks through metadata like time stamps & unique IDs.
- Integrate notebooks into your team's project management & data platform.
- Track data flow in and out of notebooks: Treat notebooks as analytics steps in a wider inference graph of collaborative R&D.

Install:

```
pip install nbproject
```

At the top of any notebook, call

```
from nbproject import header
```

This will both initialize `nbproject` and interactively display notebook metadata! Done.

For more functionality, check out the [API reference](api) and the [guides](guides/index)!

```{toctree}
:maxdepth: 1
:hidden:

guides/index
api
changelog
```
