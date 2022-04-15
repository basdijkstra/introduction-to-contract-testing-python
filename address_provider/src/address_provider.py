from flask import Flask, abort, jsonify

fakedb = {}

app = Flask(__name__)


@app.route('/address/<address_id>', methods=['GET'])
def get_address_by_id(address_id):
    app.logger.info('GET request for address id %s', address_id)
    if address_id == 'this_is_not_a_valid_address_id':
        abort(400)
    address_data = fakedb.get(address_id)
    if not address_data:
        abort(404)
    response = jsonify(**address_data)
    app.logger.debug('GET address for %s returns data:\n%s', address_data, response.data)
    return response


@app.route('/address/<address_id>', methods=['DELETE'])
def delete_address_by_id(address_id):
    if address_id == 'this_is_not_a_valid_address_id':
        abort(400)
    del fakedb[address_id]
    return '', 204


if __name__ == '__main__':
    app.run(debug=True, port=5001)
