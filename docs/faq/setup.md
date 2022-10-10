# Setup guide

## Local installation

Jupyter Lab:

- any pip or conda installation
- brew installation may give a problems

Jupyter Notebook:

- any pip or conda installation

## Saturn Cloud

Runs [out-of-the-box](https://github.com/laminlabs/run-lamin-on-saturn).

## Google Cloud Vertex AI

For both managed and user-managed notebooks:

```
pip install ipylab==0.5.2 --user
pip install nbproject
```

After the installation, close the Vertex Jupyter Lab interface page and open it again.

Note: ipylab 0.6.0 is not yet compatible with current Vertex AI but likely will be in the future (2022-08-29.)

Related issue: [#214](https://github.com/laminlabs/nbproject/issues/214).
