import logging
import os

from pact import Verifier

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PACT_FILE_CUSTOMER = "customer_consumer_python-address_provider_python.json"
PACT_FILE_ORDER = "order_consumer_python-address_provider_python.json"

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 9876
PACT_URL = f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}'
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_verify_customer_contract():
    verifier = Verifier(provider='address_provider_python',
                        provider_base_url=PACT_URL)

    output, logs = verifier.verify_pacts(f'{PACT_DIR}/pacts/{PACT_FILE_CUSTOMER}',
                                         verbose=False,
                                         provider_states_setup_url="{}/_pact/provider_states".format(PACT_URL))

    assert (output == 0)


def test_verify_order_contract():
    verifier = Verifier(provider='address_provider_python',
                        provider_base_url=PACT_URL)

    output, logs = verifier.verify_pacts(f'{PACT_DIR}/pacts/{PACT_FILE_ORDER}',
                                         verbose=False,
                                         provider_states_setup_url="{}/_pact/provider_states".format(PACT_URL))

    assert (output == 0)