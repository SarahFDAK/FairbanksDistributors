from . import db

from flask import jsonify


def load_chips():
    return _load_items('Chips')


def load_freezer_bread():
    return _load_items('Freezer Bread')


def load_fresh_bread():
    return _load_items('Fresh Bread')


class Item:
    def __init__(self, item_id, item_name, category_name, ounces, pack_quantity, upc):
        self.item_id = item_id
        self.item_name = item_name
        self.category_name = category_name
        self.ounces = ounces
        self.pack_quantity = pack_quantity
        self.upc = upc

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    def to_dict(self):
        return {
            'name': self.item_name,
            'case': self.default(self.pack_quantity),
            'oz': self.default(self.ounces),
            'upc': self.default(self.upc),
            'id': self.item_id
        }

    def default(self, val, default_val=''):
        return val if val is not None else default_val


def _load_items(item_type):
    with db.connect() as connection:
        try:
            cursor = connection.cursor()
            query = _items_query()
            cursor.execute(query, (f'{item_type}',))
            item_rows = cursor.fetchall()

            items = [
                Item.from_row(row) for row in item_rows
            ]

            categories = _unique([item.category_name for item in items])

            items_by_categories = {
                category_name: [] for category_name in categories
            }

            for item in items:
                items_by_categories[item.category_name].append(item.to_dict())

            website_format = []
            for category_name, category_items in items_by_categories.items():
                website_format.append({
                    'name': category_name,
                    'items': category_items
                })

            return jsonify({
                'categories': website_format
            })

        except Exception as e:
            raise e
            return jsonify({
                'error': str(e)
            })


def _unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def _items_query():
    return f'''
        SELECT item_id,
               item_name,
               category_name,
               ounces,
               pack_quantity,
               upc
          FROM category_types
                 JOIN categories ON category_types.type_id = categories.type_id
                 JOIN items ON categories.category_id = items.category_id
         WHERE type_name = %s
           AND is_active = TRUE
         ORDER BY department, category_name, line_number, item_name;
    '''
