import logging
import os

import pytest
from pact import Consumer, Like, Provider, Format, Term

from order_consumer.src.payment_consumer import PaymentConsumer

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
print(Format().__dict__)

PACT_MOCK_HOST = '127.0.0.1'
PACT_MOCK_PORT = 9876
PACT_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/pacts'

EXISTING_ORDER = 'e15a4786-240b-486f-83cc-74bb925eec1d'


@pytest.fixture
def consumer():
    return PaymentConsumer(
        f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}'
    )


@pytest.fixture(scope='session')
def pact():
    pact = Consumer('order_consumer_python').has_pact_with(
        Provider('ideal'),
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


def test_get_existing_payment_id(pact, consumer):

    expected = {
        'id': Format().uuid,
        'order_id': Format().uuid,
        'amount': Like(100),
        'status': Term(r"open|paid|rejected", "paid")
    }

    (pact
     .given(f'Payment for order with ID {EXISTING_ORDER} exists')
     .upon_receiving('GET payment data - order exists')
     .with_request('get', f'/order/{EXISTING_ORDER}/payment')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        payment = consumer.get_payment_for_order(EXISTING_ORDER)
        assert payment.amount == 100
        assert payment.status == 'paid'
