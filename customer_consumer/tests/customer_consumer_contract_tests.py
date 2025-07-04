import os

import pytest
from pact import Consumer, Like, Provider, Format

from customer_consumer.src import AddressClient

PACT_MOCK_HOST = '127.0.0.1'
PACT_MOCK_PORT = 9876
PACT_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/pacts'

EXISTING_ADDRESS = '8aed8fad-d554-4af8-abf5-a65830b49a5f'
NONEXISTENT_ADDRESS = '00000000-0000-0000-0000-000000000000'
INVALID_ADDRESS = 'this_is_not_a_valid_address_id'


@pytest.fixture
def address_client():
    return AddressClient(
        f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}'
    )


@pytest.fixture(scope='session')
def pact():
    pact = Consumer('customer_consumer_python').has_pact_with(
        provider=Provider('address_provider_python'),
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


def test_get_existing_address_id(pact, address_client):
    expected = {
        'id': Format().uuid,
        'street': Like('Main Street'),
        'number': Like(123),
        'city': Like('Nothingville'),
        'zipcode': Like(90210),
        'state': Like('Tennessee')
    }

    (pact
     .given(f'Address with ID {EXISTING_ADDRESS} exists')
     .upon_receiving('GET address data - address exists')
     .with_request('get', f'/address/{EXISTING_ADDRESS}')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        address = address_client.get_address(EXISTING_ADDRESS)
        assert address.street == 'Main Street'
        assert address.number == 123
        assert address.city == 'Nothingville'
        assert address.zipcode == 90210
        assert address.state == 'Tennessee'


def test_get_nonexistent_address_id(pact, address_client):
    (pact
     .given(f'Address with ID {NONEXISTENT_ADDRESS} does not exist')
     .upon_receiving('GET address data - address does not exist')
     .with_request('get', f'/address/{NONEXISTENT_ADDRESS}')
     .will_respond_with(404))

    with pact:
        address = address_client.get_address(NONEXISTENT_ADDRESS)
        assert address is None


def test_get_invalid_address_id(pact, address_client):
    (pact
     .given('No specific state required')
     .upon_receiving('GET address data - address ID is invalid')
     .with_request('get', f'/address/{INVALID_ADDRESS}')
     .will_respond_with(400))

    with pact:
        address = address_client.get_address(INVALID_ADDRESS)
        assert address is None


def test_delete_address_id(pact, address_client):
    (pact
     .given('No specific state required')
     .upon_receiving('DELETE address data - address ID is valid')
     .with_request('delete', f'/address/{EXISTING_ADDRESS}')
     .will_respond_with(204))

    with pact:
        address_client.delete_address(EXISTING_ADDRESS)
