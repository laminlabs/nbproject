```{include} ../README.md
:start-line: 0
:end-line: 4
```

Features:

- Keep track of notebooks through metadata like time stamps, versions & unique IDs.
- Make notebooks reproducible through dependency & integrity tracking.
- Integrate notebooks into your team's project management & data platform.
- Integrate with [LaminDB](https://lamin.ai/lamindb) to track data flow in and out of notebooks. Notebooks are analytics steps in an inference graph of collaborative R&D.

Supported editors:

- Jupyter Lab (best experience)
- VScode & Jupyter Notebook (no interactive experience, some quirks)

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
