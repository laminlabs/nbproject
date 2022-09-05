```{include} ../README.md
:start-line: 0
:end-line: 7
```

_Open-source ELN for the drylab._

Manage notebooks with metadata, dependency, and integrity tracking.
Sketch pipelines and share reproducible notebooks with context.

Supported editors & platforms:

- Jupyter Lab
  - Google Cloud Vertex AI (see [setup guide](faq/setup))
  - brew-installed Jupyter Lab may give problems, please install via `pip install jupyterlab` or conda
- Jupyter Notebook
- VS Code (no interactive experience, not recommended for production)

Install:

```
pip install nbproject
```

Get started:

```
from nbproject import header; header()  # Initializes & displays metadata, starts tracking. Done. 😅
```

Documentation:

- [Quickstart](quickstart) and [guide](guide/index).
- See the [API reference](api).
- If you get stuck, see [FAQ](faq/index) for edge cases & errors.

```{toctree}
:maxdepth: 1
:hidden:

guide/index
api
faq/index
changelog
```
