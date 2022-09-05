# Manage a collection of notebooks with the CLI

Here we consider that you have a collection of existing notebooks that you'd like to become

- more reproducible through pypackage tracking
- more findable & integrated through project management metadata

```{warning}
This implementation is subject to change. We'll offer better & better ways of integrating databases and a distributed metadata store.
```

## Initialize nbproject

Use the CLI to init `nbproject` for a collection of notebooks like this:

```
$ cd my_notebook_collection/
$ nbproject init
created my_notebook_collection/nbproject_metadata.yml
```

Now all notebooks contain the initial nbproject metadata fields.
The `nbproject_metadata.yml` file shows you the metadata fields for each notebook, and serves as a metadata "database" for the project.

You'll of course also see these metadata fields in each notebook, as usual, when calling:

```
from nbproject import header
```

## Synchronize changes

If you have any changes in the metadata of the notebooks of your project, changes in location of a notebook within the project directory, additions of new notebooks, renamings etc., you can synchronize everything with `nbproject_metadata.yml` via

```
$ nbproject sync .
synchronized my_notebook_collection/nbproject_metadata.yml
```

Passing `.` to `nbproject sync` synchronizes the whole root directory of you project.
You can also pass a list of paths within you project to synchronize only specific notebooks.

## Infer pypackages

To automatically infer pypackages from the notebooks of your project, use the option `--deps` (or `-d`):

```
$ nbproject sync . --deps
synchronized my_notebook_collection/nbproject_metadata.yml
```

This command parses the notebooks, infers all pypackages within the notebooks with their versions
from the current python environment and writes them to metadata of the notebooks.

## Pin pypackages

If you want to avoid pining the pypackages versions, use the option `--no-versions` (or `-nv`):

```
$ nbproject sync . --deps --no-versions
synchronized my_notebook_collection/nbproject_metadata.yml
```

## Publish a list of notebooks

You can use CLI to publish a list of notebooks (see the publish tutorial also):

```
$ nbproject publish notebook.ipynb another_notebook.ipynb
published 2 notebooks.
```

## Generate a requirements file

To generate a `requirements.txt` for a list of notebooks of the project, run:

```
$ nbproject reqs .
created my_notebook_collection/requirements.txt
```

Again, passing `.` means that `requirements.txt` is created for all notebooks of your project.
To create the file only for specific notebooks, pass the list of their paths.
