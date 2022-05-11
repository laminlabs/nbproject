# nbproject: Manage Jupyter notebooks

- Make your data science projects reproducible through dependency tracking.
- Keep track of the notebooks themselves through time stamps, unique IDs & metadata. Integrate into your team's project management software & data platform.
- Track data flow in and out of notebooks. Treat notebooks as analytics steps in a wider inference graph of collaborative R&D.

---

Install via:

```
$ pip install nbproject
```

At the top of any notebook, call

```
from nbproject import header
```

This will both initialize `nbproject` and interactively display notebook metadata! Done.

For more functionality, check out the [guides](guides)! A comprehensive API documentation is to come.

```{toctree}
:maxdepth: 1
:hidden:

guides
```
