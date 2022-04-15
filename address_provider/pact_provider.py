from flask import jsonify, request
from src import app, fakedb

EXISTING_ADDRESS = '8aed8fad-d554-4af8-abf5-a65830b49a5f'


@app.route('/_pact/provider_states', methods=['POST'])
def provider_states():
    mapping = {
        'Customer GET: the address ID matches an existing address': setup_address_data,
        'Customer GET: the address ID does not match an existing address': setup_no_address_data,
        'Customer GET: the address ID is invalid': setup_address_data,
        'Customer DELETE: the address ID is valid': setup_address_data,
        'Customer DELETE: the address ID is invalid': setup_address_data,
        'Order GET: the address ID matches an existing address': setup_address_data,
        'Order GET: the address ID does not match an existing address': setup_no_address_data,
        'Order GET: the address ID is invalid': setup_address_data,
        'Order DELETE: the address ID is valid': setup_address_data,
        'Order DELETE: the address ID is invalid': setup_address_data
    }
    mapping[request.json['state']]()
    return jsonify({'result': request.json['state']})


def setup_no_address_data():
    if EXISTING_ADDRESS in fakedb:
        del fakedb[EXISTING_ADDRESS]


def setup_address_data():

    fakedb[EXISTING_ADDRESS] = {
        'id': EXISTING_ADDRESS,
        'street': 'Main Street',
        'number': 123,
        'city': 'Nothingville',
        'zip_code': 90210,
        'state': 'Tennessee'
    }


if __name__ == '__main__':
    app.run(debug=True, port=9876)
