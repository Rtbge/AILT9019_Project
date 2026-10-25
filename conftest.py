"""
conftest.py – pytest hooks shared across all test files.

Adds the --run-live flag used by TestLiveSmoke in test_backend.py.
"""

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="Run the live API smoke test (requires real API credentials).",
    )
