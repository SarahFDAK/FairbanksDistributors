import xlrd
import csv
import math
import json


def csv_from_excel():
    wb = xlrd.open_workbook('/tmp/chipForm.xls')
    sh = wb.sheet_by_index(0)
    your_csv_file = open('output.csv', 'w', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def get_data(xls_path):
    book = xlrd.open_workbook(xls_path)
    sheet = book.sheet_by_index(0)
    num_pages = int(math.ceil(sheet.nrows // 69))
    return_data = []
    for page in range(num_pages):
        row_range = range(page*72, min(page*72+72, sheet.nrows))
        return_data += [[sheet.cell_value(r, c) for c in range(0, 5)] for r in row_range] + \
                       [[sheet.cell_value(r, c) for c in range(5, 10)]
                        for r in row_range]
    return return_data


def is_category(row):
    not_categories = ['', 'Bridges', 'TMD Bottoms', 'TMD Tops', 'Clipstrips', 'Weekenders',
                      '4X4 Display', 'Rolling Dip Rack']
    return '-' not in row[3] and row[1] not in not_categories


def get_categories(data):
    return [row[1].strip() for row in data if is_category(row)]


def get_items(data):
    return [row[1] for row in data if not is_category(row) and row[1] != '']


def get_chips_by_category(data):
    all_items, current_category = {category: []
                                   for category in get_categories(data)}, None
    for row in data:
        if is_category(row):
            current_category = row[1].strip()
        elif row[1] != '':
            name, oz, upc, case = row[1:]
            print(name.strip())

            item = {
                'name': name.strip(),
                'oz': oz,
                'upc': upc,
                'case': case
            }

            all_items[current_category].append(item)

    return {
        "categories": [
            {"name": category_name, "items": items}
            for (category_name, items) in all_items.items()
        ]
    }


if __name__ == "__main__":
    csv_from_excel()
    data = get_data()
