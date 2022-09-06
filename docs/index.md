```{include} ../README.md
:start-line: 0
:end-line: 6
```

Open-source ELN for the drylab.

- Manage notebooks with metadata, dependency, and integrity tracking.
- Sketch pipelines and share reproducible notebooks with context.

Why? Read the [report](https://lamin.ai/reports/2022/nbproject).

Supported editors & platforms:

- Jupyter Lab
  - Google Cloud Vertex AI (see [setup guide](faq/setup))
  - brew-installed Jupyter Lab may give problems, please install via `pip install jupyterlab` or conda
- Jupyter Notebook
- VS Code (no interactive experience, not recommended for production)

Install: ![pyversions](https://img.shields.io/pypi/pyversions/nbproject)

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
