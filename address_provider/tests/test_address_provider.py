import logging
import os

from pact import Verifier

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PACT_FILE_CUSTOMER = "customer_consumer_python-address_provider_python.json"
PACT_FILE_ORDER = "order_consumer_python-address_provider_python.json"

APP_HOST = '127.0.0.1'
APP_PORT = 9876
APP_URL = f'http://{APP_HOST}:{APP_PORT}'
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_verify_customer_contract():
    verifier = Verifier(provider='address_provider_python',
                        provider_base_url=APP_URL)

    output, logs = verifier.verify_pacts(
        f'{PACT_DIR}/pacts/{PACT_FILE_CUSTOMER}',
        verbose=False,
        provider_states_setup_url=f'{APP_URL}/_pact/provider_states'
    )

    assert (output == 0)
