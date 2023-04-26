[![Stars](https://img.shields.io/github/stars/laminlabs/nbproject?logo=GitHub&color=yellow)](https://github.com/laminlabs/nbproject)
[![coverage](https://codecov.io/gh/laminlabs/nbproject/branch/main/graph/badge.svg?token=05R04PR9RB)](https://codecov.io/gh/laminlabs/nbproject)
[![pypi](https://img.shields.io/pypi/v/nbproject?color=blue&label=pypi%20package)](https://pypi.org/project/nbproject)
[![doi](https://img.shields.io/badge/doi-10.56528%2Fnbp-lightgrey)](https://doi.org/10.56528/nbp)

# nbproject: Light-weight Jupyter notebook tracker

Track & publish notebooks with their metadata, dependencies, and integrity.

💡 Consider [lamindb.track](https://lamin.ai/docs/lamindb.track) instead of nbproject:

- `nbproject` will mostly be maintained as a backend for `lamindb.track()`
- `lamindb.track()` consistently tracks data sources across notebooks, pipelines & apps
- `lamindb` gives you full provenance for datasets that you pull and push from a notebook
- `lamindb.track()` also knows how to manage _duplicated_ notebooks & integrates with Google Colab
- Like `nbproject`, `lamindb` is open-source

---

Supported editors & platforms:

- Jupyter Lab
  - any pip or conda installation, a brew installation may give a problems
  - Saturn Cloud ([run](https://github.com/laminlabs/run-lamin-on-saturn))
  - Google Cloud Vertex AI (see [setup faq](faq/setup))
- Jupyter Notebook
- VS Code (no interactive experience, not recommended for production)

For broader support and features, see `lamindb.track()`.

Install: ![pyversions](https://img.shields.io/pypi/pyversions/nbproject)

```
pip install nbproject
```

Get started:

```
import nbproject

nbproject.header()  # Tracks notebook, displays metadata

# do things

nbproject.publish()  # Checks consecutiveness, bumps version
```

More: Read the [docs](https://lamin.ai/docs/nbproject).
