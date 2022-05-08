# nbproject: Manage your notebooks

Start treating your Jupyter notebooks like gems, keep track of them and the data they load and write, share and collaborate at scale.

- Turn every notebook into a Notion database page.
- Treat every Jupyter notebook like you'd treat an ELN on Benchling.

## Specification in comparison to other references

- Add metadata to notebooks first issue mentioned: https://github.com/jupyter/nbformat/issues/148
  - This triggered cell-level IDs, but left notebook-level IDs unresolved: https://nbformat.readthedocs.io/en/latest/format_description.html#cell-ids
- nbproject is client/distributed/embedded, and not on the server side:
  - https://github.com/nteract/commuter (see Netflix: https://netflixtechblog.com/notebook-innovation-591ee3221233)
  - https://github.com/notebook-sharing-space/nbss
- nbproject offers only the metadata management related project & data management, which JupyterBook doesn't. The focus of the https://github.com/executablebooks is publication.
  - Metadata within Jupyterbook is discussed here: https://jupyterbook.org/content/metadata.html
- Server-side notebook platforms have adopted providing IDs and other metadata to notebooks for a _long_ time already

## Notebook platforms

For instance, Google Colab has IDs just as any other notebook platform

```
  "metadata": {
    "colab": {
      "provenance": [
        {
          "file_id": "1Rgt3Q7hVgp4Dj8Q7ARp7G8lRC-0k8TgF",
          "timestamp": 1560453945720
        },
        {
          "file_id": "https://gist.github.com/blois/057009f08ff1b4d6b7142a511a04dad1#file-post_run_cell-ipynb",
          "timestamp": 1560453945720
        }
      ],
```

Other notebook platforms:

- Binder | [https://mybinder.org/](https://mybinder.org/)
- Saturn Cloud | [https://saturncloud.io/](https://saturncloud.io/)
- Google Colab, Colab Pro, and within Google Cloud:
  - [https://research.google.com/colaboratory/marketplace.html](https://research.google.com/colaboratory/marketplace.html)
  - [https://colab.research.google.com/signup](https://colab.research.google.com/signup)
  - [https://cloud.google.com/automl-tables/docs/notebooks](https://cloud.google.com/automl-tables/docs/notebooks)
    - [https://github.com/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/tables/census_income_prediction/getting_started_notebook.ipynb](https://github.com/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/tables/census_income_prediction/getting_started_notebook.ipynb)
- AWS sagemaker | [https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks.html](https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks.html)
- Gradient | [https://gradient.run/notebooks](https://gradient.run/notebooks)
- Jupyter hub | [https://jupyter.org/hub](https://jupyter.org/hub)
- Deepnote | [https://deepnote.com/](https://deepnote.com/)
- Jovian | [https://jovian.ai/docs/](https://jovian.ai/docs/)
- Bookstore | [nteract/bookstore](https://www.notion.so/nteract-bookstore-ae0cd2f869f842be9027835f02ca6421)
- Commuter | [nteract/commuter](https://www.notion.so/nteract-commuter-5bc5657c78b2436fb66b8b9a76520226)

## Features

- Metadata display with a **configurable schema** as in Notion (have some fields be visible and others not?)
- ID generation and managemenet
- Notebook integrity & status
  - relevant for depositing data that comes from a "clean notebook"
    - distinguish "save deposit", all cells have been executed sequentially, no cell has been deleted from "rapid deposit" - which annotates with a warning - in which cells have been incompletely or multiple times executed
  - relevant for data provenance at loading time
    - tell user whether a notebook has already been instantiated, has been used to deposit data, if so, potentially show graph
    - tell user that no data was ever deposited with the notebook
