import requests


class AddressConsumer(object):

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_address(self, address_id):
        """GET an address from the provider by its id"""
        uri = f'{self.base_uri}/address/{address_id}'
        response = requests.get(uri)
        if response.status_code in (400, 404):
            return None
        response_json = response.json()
        return Address(
            response_json['id'],
            response_json['street'],
            response_json['number'],
            response_json['city'],
            response_json['zipcode'],
            response_json['state']
        )

    def delete_address(self, address_id):
        """DELETE an address at the provider by its id"""
        uri = f'{self.base_uri}/address/{address_id}'
        requests.delete(uri)


class Address(object):

    def __init__(self, address_id, street, number, city, zipcode, state):
        self.address_id = address_id
        self.street = street
        self.number = number
        self.city = city
        self.zipcode = zipcode
        self.state = state
