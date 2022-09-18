import nox

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "tests"


@nox.session(python=["3.10"], name="format")
def format_(session):
    args = session.posargs or locations
    session.run(
        "poetry",
        "install",
        "--without",
        "main",
        "--with",
        "format",
        external=True,
    )
    session.run("black", *args)
    session.run("isort", *args)


@nox.session(python=["3.10"])
def lint(session):
    args = session.posargs or locations
    session.run(
        "poetry",
        "install",
        "--without",
        "main",
        "--with",
        "format",
        external=True,
    )
    session.run("flake8", *args)
    session.run("black", "--check", *args)
    session.run("isort", "--check", *args)


@nox.session(python=["3.10"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--with", "test")
    session.run("pytest", *args)
