```{include} ../README.md
:start-line: 0
:end-line: 1
```

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

If you want more configuration, call the class

```
from nbproject import Header
header = Header(*args, **kwargs, show=False)
header.infer_dependencies()
header.add_dependency("pytorch")
header.check_for_integrity()
header.show()
```

For more functionality, check out the [guides](guides)! A comprehensive API documentation is to come.

```{toctree}
:maxdepth: 1
:hidden:

guides
api
```
