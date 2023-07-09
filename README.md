[![Stars](https://img.shields.io/github/stars/laminlabs/nbproject?logo=GitHub&color=yellow)](https://github.com/laminlabs/nbproject)
[![coverage](https://codecov.io/gh/laminlabs/nbproject/branch/main/graph/badge.svg?token=05R04PR9RB)](https://codecov.io/gh/laminlabs/nbproject)
[![pypi](https://img.shields.io/pypi/v/nbproject?color=blue&label=pypi%20package)](https://pypi.org/project/nbproject)
[![doi](https://img.shields.io/badge/doi-10.56528%2Fnbp-lightgrey)](https://doi.org/10.56528/nbp)

# nbproject

Light-weight Jupyter notebook manager. Track metadata, imports, and integrity.

---

💡 We recommend [lamindb.track()](docs:lamindb.track) instead of `nbproject` to:

- consistently track data sources across notebooks, pipelines & apps
- full provenance for datasets that you pull and push from notebooks
- manage notebook copying & integrate with Google Colab

Like `nbproject`, `lamindb` is open-source.

`nbproject` will continue to be maintained as a utility for `lamindb`.

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
