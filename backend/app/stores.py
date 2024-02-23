import json

from flask import jsonify
from . import db


class Store:
    def __init__(self, id, name, chain_id):
        self.id = id
        self.name = name
        self.chain_id = chain_id

    @classmethod
    def from_row(cls, row):
        id, name, chain_id = row
        return cls(id, name, chain_id)

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id
        }


def load():
    with db.connect() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM stores;')
            stores = cursor.fetchall()

            store_dicts = [
                Store.from_row(row).to_dict() for row in stores
            ]

            return jsonify(store_dicts)

        except Exception as e:
            return jsonify({
                'error': str(e)
            })
