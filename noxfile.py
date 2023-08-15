import nox
from laminci import move_built_docs_to_docs_slash_project_slug
from laminci.nox import build_docs, run_pre_commit, run_pytest

nox.options.default_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def build(session):
    session.run(*"pip install .[dev]".split())
    run_pytest(session)
    build_docs(session)
    move_built_docs_to_docs_slash_project_slug()
