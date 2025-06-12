from __future__ import annotations

import os
import time
import logging
from datetime import datetime, timezone
from multiprocessing import Process
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock

import pytest
from yarl import URL

from flask import request
from pact import Verifier  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from collections.abc import Generator
from address_provider.src.address_provider import app, Address

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

PROVIDER_HOST = '127.0.0.1'
PROVIDER_PORT = 9876
PROVIDER_URL = URL(f'http://{PROVIDER_HOST}:{PROVIDER_PORT}')

@app.route
def pact_provider_states() -> dict[str, str | None]:

    if request.json is None:
        raise ValueError('Supplied request body must be in JSON format')

    state: str = request.json["state"]

    mapping = {
        "Address with ID 8aed8fad-d554-4af8-abf5-a65830b49a5f exists": address_exists,
        "Address with ID 00000000-0000-0000-0000-000000000000 does not exist": address_does_not_exist,
        "No specific state required": no_specific_state_required
    }

    return {"result": mapping[state]()}  # type: ignore[index]

def run_server() -> None:
    """
    Run the Flask server.

    This function is required to run the Flask server in a separate process. A
    lambda cannot be used as the target of a `multiprocessing.Process` as it
    cannot be pickled.
    """
    app.run(
        host=PROVIDER_URL.host,
        port=PROVIDER_URL.port,
    )

@pytest.fixture(scope="module")
def verifier() -> Generator[Verifier, Any, None]:
    """Set up the Pact verifier."""
    proc = Process(target=run_server, daemon=True)
    verifier = Verifier(
        provider="address_provider_python",
        provider_base_url=str(PROVIDER_URL),
    )
    proc.start()
    time.sleep(2)
    yield verifier
    proc.kill()


def address_exists() -> None:

    import address_provider.src.address_provider

    address_provider.src.address_provider.FAKE_DB = MagicMock()
    address_provider.src.address_provider.FAKE_DB.get.return_value = Address(
        id = "8aed8fad-d554-4af8-abf5-a65830b49a5f",
        street = "Some street",
        number = 456,
        city = "Some city",
        zipcode = 87654,
        state = "Some state",
    )

def address_does_not_exist() -> None:

    import address_provider.src.address_provider

    address_provider.src.address_provider.FAKE_DB = MagicMock()
    address_provider.src.address_provider.FAKE_DB.get.return_value = None

def no_specific_state_required() -> None:
    pass

def test_against_broker(verifier: Verifier) -> None:
    """
    Test the provider against the broker.

    The broker will be used to retrieve the contract, and the provider will be
    tested against the contract.

    As Pact is a consumer-driven, the provider is tested against the contract
    defined by the consumer. The consumer defines the expected request to and
    response from the provider.

    For an example of the consumer's contract, see the consumer's tests.
    """
    code, _ = verifier.verify_with_broker(
        broker_url=os.environ.get("PACT_BROKER_BASE_URL"),
        # Despite the auth being set in the broker URL, we still need to pass
        # the username and password to the verify_with_broker method.
        broker_token=os.environ.get("PACT_BROKER_TOKEN"),
        publish_version="1.0.0",
        publish_verification_results=True,
        provider_states_setup_url=f'{PROVIDER_URL}/_pact/provider_states',
    )

    assert code == 0