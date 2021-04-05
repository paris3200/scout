"""Nox Sessions."""
import tempfile

import nox
from nox_poetry import session
from nox_poetry.sessions import Session

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "mypy", "pytype", "safety", "tests"


@session(python=["3.7", "3.8", "3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-cov", ".")
    session.run("pytest", "--cov")


@session(python=["3.8", "3.9"])
def lint(session: Session) -> None:
    """Run the lint session."""
    args = session.posargs or locations
    session.install(
        "flake8", "flake8-annotations", "flake8-black", "flake8-bugbear", "flake8-isort"
    )
    session.run("flake8", *args)


@session(python="3.9")
def black(session: Session) -> None:
    """Run black session."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python="3.9")
def safety(session: Session) -> None:
    """Run the safety session."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@session(python="3.9")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@session(python="3.8")
def pytype(session: Session) -> None:
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)
