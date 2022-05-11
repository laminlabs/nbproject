# Using the CLI to initialize the project and infer dependencies

To init the project, `cd` to the folder where you want to initialize your project and run the `nbproject` cli with the `init` command.

```
>> nbproject init
Created /your/project/nbproject_metadata.yml
```

You have initialized your project. Now all the notebooks contain the initial nbproject metadata fields. The root folder of your project contains the file `nbproject_metadata.yml`. This file shows you the nbproject metadata fields for each notebook, you can also see these fields in each notebook using python

```
from nbproject import header
```

If you have any changes in the metadata of the notebooks of your project, changes in location of a notebook within the project folder, additions of new notebooks, renamings etc., you can synchronize everything with `nbproject_metadata.yml` using the command

```
>> nbproject sync .
Synchronized /your/project/nbproject_metadata.yml
```

`.` synchronizes the whole root folder of you project, you can also pass a list of specific paths within you project to synchronize only the notebooks in these paths.

To automatically infer dependencies from the notebooks of your project, use the option `--deps` (or `-d`)

```
>> nbproject sync . --deps
Synchronized /your/project/nbproject_metadata.yml
```

This command parses the notebooks, infers all dependencies (python packages based on `import`) within the notebooks and writes them to metadata of the notebooks. As before, the dependencies metadata fields can also be seen in `nbproject_metadata.yml`.

To infer dependencies and also pin the packages' versions from the current python environment, you can use the option `--version` (or `-v`)

```
>> nbproject sync . --deps --versions
Synchronized /your/project/nbproject_metadata.yml
```

To generate `requirments.txt` for a list of notebooks of the project, run

```
>> nbproject reqs .
Created /your/project/requirments.txt
```

`.` means that `requirments.txt` is created for all notebooks of your projetc, to create the file only for some notebooks, pass the list of their paths instead `.` to the command above.
