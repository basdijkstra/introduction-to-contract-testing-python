import logging
import os

import pytest
from pact import Consumer, Like, Provider, Format

from order_consumer.src import AddressConsumer

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
print(Format().__dict__)

PACT_MOCK_HOST = '127.0.0.1'
PACT_MOCK_PORT = 9876
PACT_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/pacts'

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
    pact = Consumer('order_consumer_python').has_pact_with(
        Provider('address_provider_python'),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
        publish_to_broker=False
    )

    print('start service')
    pact.start_service()

    yield pact
    print('stop service')
    pact.stop_service()


def test_get_existing_address_id(pact, consumer):
    """
    Add two fields to the expected response:
    - one field 'zipcode', which should be an integer
    - another field 'residential', which should be a boolean

    Also add assertions that check that the added response fields
    will be parsed and read correctly if returned by the provider.
    """

    expected = {
        'id': Format().uuid,
        'street': Like('Main Street'),
        'number': Like(123),
        'city': Like('Nothingville')
    }

    (pact
     .given(f'Address with ID {EXISTING_ADDRESS} exists')
     .upon_receiving('GET address data - address exists')
     .with_request('get', f'/address/{EXISTING_ADDRESS}')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        address = consumer.get_address(EXISTING_ADDRESS)
        assert address.street == 'Main Street'
        assert address.number == 123
        assert address.city == 'Nothingville'

def test_get_nonexistent_address(pact, consumer):
    """
    Implement this test by completing the following steps:
    - Define the pact, including a provider state 'Address with ID {NONEXISTENT_ADDRESS} does not exist'
    - Specify the request and expect the provider to return an HTTP 404. You don't need to add expectations for the response body
    - call the get_address() method on the consumer object using NONEXISTENT_ADDRESS as an argument
    - assert that the response is equal to None
    """
    pass

def test_get_invalid_address_id(pact, consumer):
    """
    Implement this test by completing the following steps:
    - Define the pact, including a provider state 'No specific state required'
    - Specify the request and expect the provider to return an HTTP 400. You don't need to add expectations for the response body
    - call the get_address() method on the consumer object using INVALID_ADDRESS as an argument
    - assert that the response is equal to None
    """
    pass
