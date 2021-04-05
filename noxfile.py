"""Nox Sessions."""
import tempfile

import nox
from nox_poetry import session
from nox_poetry.sessions import Session

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "safety", "tests"


@session(python=["3.7", "3.8", "3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-cov", ".")
    session.run("pytest", "--cov")


@session(python=["3.8", "3.9"])
def lint(session: Session) -> None:
    """Run the lint session."""
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-bugbear", "flake8-isort")
    session.run("flake8", *args)


@session(python="3.9")
def black(session):
    """Run black session."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python="3.9")
def safety(session):
    """run the safety session."""
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
