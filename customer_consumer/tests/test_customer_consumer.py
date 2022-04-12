import logging
import os
import atexit

import pytest
from pact import Consumer, Like, Provider, Format

from customer_consumer.src import AddressConsumer

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
print(Format().__dict__)

PACT_BROKER_URL = "https://ota.pactflow.io"
PACT_FILE = "customer_consumer_python-address_provider_python.json"
PACT_BROKER_TOKEN = "HbtH0tZq7CU4d18JlKR2kA"

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234
PACT_DIR = os.path.dirname(os.path.realpath(__file__))

EXISTING_ADDRESS = '8aed8fad-d554-4af8-abf5-a65830b49a5f'
NONEXISTENT_ADDRESS = '00000000-0000-0000-0000-000000000000'
INVALID_ADDRESS = 'this_is_not_a_valid_address_id'


@pytest.fixture
def consumer():
    return AddressConsumer(
        f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}'
    )


@pytest.fixture(scope='session')
def pact():
    pact = Consumer('customer_consumer_python', version='1.0.0').has_pact_with(
        Provider('address_provider_python'), host_name=PACT_MOCK_HOST, port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR, publish_to_broker=False, broker_base_url=PACT_BROKER_URL,
        broker_token=PACT_BROKER_TOKEN)

    print('start service')
    pact.start_service()
    atexit.register(pact.stop_service)

    yield pact
    print('stop service')
    pact.stop_service()


def test_get_existing_address_id(pact, consumer):
    expected = {
        'id': Format().uuid,
        'street': Like('Main Street'),
        'number': Like(123),
        'city': Like('Nothingville'),
        'zip_code': Like(90210),
        'state': Like('Tennessee')
    }

    (pact
     .given('Customer GET: the address ID matches an existing address')
     .upon_receiving('a request for address data')
     .with_request('get', f'/address/{EXISTING_ADDRESS}')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        address = consumer.get_address(EXISTING_ADDRESS)
        assert address.street == 'Main Street'
        assert address.number == 123
        assert address.city == 'Nothingville'
        assert address.zip_code == 90210
        assert address.state == 'Tennessee'


def test_get_nonexistent_address_id(pact, consumer):
    (pact
     .given('Customer GET: the address ID does not match an existing address')
     .upon_receiving('a request for address data')
     .with_request('get', f'/address/{NONEXISTENT_ADDRESS}')
     .will_respond_with(404))

    with pact:
        address = consumer.get_address(NONEXISTENT_ADDRESS)
        assert address is None


def test_get_invalid_address_id(pact, consumer):
    (pact
     .given('Customer GET: the address ID is invalid')
     .upon_receiving('a request for address data')
     .with_request('get', f'/address/{INVALID_ADDRESS}')
     .will_respond_with(400))

    with pact:
        address = consumer.get_address(INVALID_ADDRESS)
        assert address is None
