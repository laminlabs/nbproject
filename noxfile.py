import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def test(session):
    session.install(".[dev, test]")
    session.run("pytest", "-s")  # write output instead of capturing it (more verbose)


@nox.session
def docs(session: nox.Session):
    session.install("-r", "docs/lamin_sphinx/requirements.txt")
    session.run(*"sphinx-build -b html source _build/html".split())
