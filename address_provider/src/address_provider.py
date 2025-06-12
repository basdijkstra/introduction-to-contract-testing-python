import logging
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from flask import Flask, jsonify, Response, request

logger = logging.getLogger(__name__)
app = Flask(__name__)

@dataclass
class Address:

    id: str
    street: str
    number: int
    city: str
    zipcode: int
    state: str

    def __post_init__(self):
        """Check that the ID provided is a valid UUID"""
        try:
            UUID(self.id)
        except ValueError:
            msg = f'{self.id} is not a valid UUID'
            logger.error(msg)
            raise ValueError(msg)

    def dict(self) -> dict[str, Any]:
        """Returns the address as a dictionary"""
        return {
            'id': self.id,
            'street': self.street,
            'number': self.number,
            'city': self.city,
            'zipcode': self.zipcode,
            'state': self.state
        }

FAKE_DB: dict[str, Address] = {}

@app.route('/address/<string:address_id>', methods=['GET'])
def get_address_by_id(address_id: str) -> Response | tuple[Response, int]:
    """Retrieves a user by their ID"""
    try:
        UUID(address_id)
    except ValueError:
        return jsonify({"error": "Invalid address ID"}), 400

    address = FAKE_DB.get(address_id)
    if not address:
        return jsonify({"error": "Address not found"}), 404

    return jsonify(address.dict()), 200

@app.route('/address/', methods=['POST'])
def create_address() -> Response | tuple[Response, int]:
    """Creates a new address"""
    if request.json is None:
        return jsonify({"error": "Invalid data supplied"}), 400

    address: dict[str, Any] = request.json

    FAKE_DB[address['id']] = Address(
        id=address['id'],
        street=address['street'],
        number=address['number'],
        city=address['city'],
        zipcode=address['zipcode'],
        state=address['state']
    )

    return jsonify(FAKE_DB[address['id']].dict()), 201

@app.route('/address/<string:address_id>', methods=['DELETE'])
def delete_address_by_id(address_id: str):
    """Deletes an address by their ID"""
    try:
        UUID(address_id)
    except ValueError:
        return jsonify({"error": "Invalid address ID"}), 400

    del FAKE_DB[address_id]
    return '', 204
