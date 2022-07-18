```{include} ../README.md
:start-line: 0
:end-line: 6
```

_Open-source ELN for the drylab._

Manage notebooks with metadata, dependency, and integrity tracking.
Sketch pipelines and share reproducible notebooks with context.

Supported editors & platforms:

- Jupyter Lab
  - Google Cloud Vertex AI ([2022-07-16](https://github.com/laminlabs/nbproject/issues/170))
- VS Code & Jupyter Notebook (no interactive experience, not recommended for production)

Install:

```
pip install nbproject
```

Get started:

```
from nbproject import header; header()  # Initializes & displays metadata, starts tracking. Done. 😅
```

Documentation:

- [Quickstart](tutorials/quickstart) and more [tutorials](tutorials/index).
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
