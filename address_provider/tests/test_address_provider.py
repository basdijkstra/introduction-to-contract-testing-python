import logging
import os

import pytest
from pact import Verifier

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PACT_BROKER_URL = 'https://ota.pactflow.io'
PACT_BROKER_TOKEN = 'HbtH0tZq7CU4d18JlKR2kA'

PACT_FILE_CUSTOMER = "customer_consumer_python-address_provider_python.json"
PACT_FILE_ORDER = "order_consumer_python-address_provider_python.json"

PACT_MOCK_HOST = '127.0.0.1'
PACT_MOCK_PORT = 9876
PACT_URL = f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}'
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def broker_options():
    return {
        "broker_url": PACT_BROKER_URL,
        "broker_token": PACT_BROKER_TOKEN,
        "publish_version": "3",
        "publish_verification_results": True,
    }


def test_verify_customer_contract(broker_options):
    verifier = Verifier(provider='address_provider_python',
                        provider_base_url=PACT_URL)

    output, logs = verifier.verify_with_broker(
        **broker_options,
        verbose=True,
        provider_states_setup_url="{}/_pact/provider_states".format(PACT_URL)
    )

    assert (output == 0)


def test_verify_order_contract(broker_options):
    verifier = Verifier(provider='address_provider_python',
                        provider_base_url=PACT_URL)

    output, logs = verifier.verify_with_broker(
        **broker_options,
        verbose=True,
        provider_states_setup_url="{}/_pact/provider_states".format(PACT_URL)
    )

    assert (output == 0)
