```{include} ../README.md
:start-line: 0
:end-line: 6
```

_Open-source ELN for the drylab._

Manage notebooks with metadata, dependency, and integrity tracking.
Sketch pipelines and share reproducible notebooks with context.

Supported editors & platforms:

- Jupyter Lab (there could be problems with non-pip/conda installations)
  - Google Cloud Vertex AI
- Jupyter Notebook
- VS Code (no interactive experience, not recommended for production)

Install:

Local:

```
pip install nbproject
```

Google Cloud Vertex AI (both managed and user-managed notebooks):

```
pip install ipylab==0.5.2 --user
pip install nbproject
```

After the installation, close the Vertex jupyter lab interface page and open it back.

Get started:

```
from nbproject import header; header()  # Initializes & displays metadata, starts tracking. Done. 😅
```

Documentation:

- [Quickstart](quickstart) and more [tutorials](tutorials/index).
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
