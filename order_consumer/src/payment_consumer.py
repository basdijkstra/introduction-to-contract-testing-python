import requests

class PaymentConsumer(object):

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_payment_for_order(self, order_id):
        """GET a payment for an order from the provider by order ID"""
        uri = f'{self.base_uri}/order/{order_id}/payment'
        response = requests.get(uri)
        if response.status_code in (400, 404):
            return None
        response_json = response.json()
        return Payment(
            response_json['id'],
            response_json['order_id'],
            response_json['amount'],
            response_json['status']
        )

class Payment(object):

    def __init__(self, payment_id, order_id, amount, status):
        self.id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.status = status
