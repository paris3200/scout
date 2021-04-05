"""Nox Sessions."""
from nox_poetry import session
from nox_poetry.sessions import Session


@session(python=["3.7", "3.8", "3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-cov", ".")
    session.run("pytest", "--cov")
