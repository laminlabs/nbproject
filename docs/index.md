```{include} ../README.md
:start-line: 0
:end-line: 1
```

Features:

- Keep track of notebooks through metadata like time stamps & unique IDs.
- Make notebooks reproducible through dependency & integrity tracking.
- Integrate notebooks into your team's project management & data platform.
- Track data flow in and out of notebooks through [LaminDB](https://lamin.ai/lamindb): Treat notebooks as analytics steps in a wider inference graph of collaborative R&D.

Supported editors:

- Jupyter Lab
- Jupyter notebook does not provide an intuitive interactive experience

Install:

```
pip install nbproject
```

Get started:

```
from nbproject import header
```

- This will initialize `nbproject`, display notebook metadata, and start tracking! Done.
- For more control, check out the [API reference](api) and the [guides](guides/index)!

```{toctree}
:maxdepth: 1
:hidden:

api
guides/index
changelog
```
