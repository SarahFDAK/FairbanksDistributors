import pytest

from app import order


def test_order(example_order):
    order.add_order_to_db(example_order)


@pytest.fixture
def example_order():
    return {
        'store': {'name': 'Test', 'id': 14},
        'items': [{
            'case': 8, 'name': "BAKED CHEETOS FLAMIN' HOT", 'oz': 7.63,
            'upc': 'FL-18391', 'amount': 3, 'type': 'BAKED - REDUCED FAT'
        }, {
            'case': 12, 'name': 'TOSTITOS SALSA MILD', 'oz': 15.5,
            'upc': 'FL-05597', 'amount': 5, 'type': 'DIPS/SALSA'
        }, {
            'case': 10, 'name': 'FRITOS FLAMIN HOT', 'oz': 9.25,
            'upc': 'FL-58931', 'amount': 2, 'type': 'FRITOS'
        }],
        'date': '2020-03-03',
        'notes': 'Test order for development'
    }
