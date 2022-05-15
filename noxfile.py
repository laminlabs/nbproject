import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def build(session):
    session.install(".[dev, test]")
    # write output instead of capturing it (more verbose)
    # disable cache
    session.run("python", "-m", "pytest", "-s", "-p", "no:cacheprovider")
    session.install("-r", "docs/lamin_sphinx/requirements.txt")
    session.run(*"sphinx-build -b html docs _build/html".split())
