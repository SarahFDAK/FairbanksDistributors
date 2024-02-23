import json
from datetime import datetime
import configparser
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes

from .write_order_xlsx import write_xlsx
from . import db


def place(order_data):
    filename = f"{str(datetime.now())}_order.xlsx" \
        .replace(' ', '_')

    try:
        order_id = add_order_to_db(order_data)
        send_order(filename, order_id, order_data)
    except Exception as e:
        return order_failure(str(e))

    return order_success(order_id)


def send_order(filename, order_id, order_data):
    write_xlsx(f"/tmp/{filename}", order_data)

    send_order_email(filename, order_id, order_data['store'])


def add_order_to_db(order_data):
    with db.connect() as connection:
        cursor = connection.cursor()

        cursor.execute(_order_query(), (
            order_data['store']['id'],
            order_data['date'],
            order_data['notes']
        ))
        order_id = cursor.fetchone()[0]

        items_query = order_items_query(
            cursor,
            order_data['items'],
            order_id
        )

        cursor.execute(items_query)
        connection.commit()

    return order_id


def _order_query():
    return f'''
        INSERT INTO orders (store_id, order_date, delivery_date, notes)
        VALUES (%s, now() - interval '9 hours', %s, %s)
        RETURNING order_id;
    '''


def order_items_query(cursor, items, order_id):

    inserts = []

    for item in items:
        tup = (str(order_id), str(item['id']), str(item['amount']))
        item_insert = cursor.mogrify(
            "(%s,%s,%s)", tup
        ).decode("utf-8")
        inserts.append(item_insert)

    args_str = ','.join(inserts)

    return f'''
    INSERT INTO ordered_items (order_id, item_id, qty_ordered)
    VALUES {args_str};
    '''


def send_order_email(filename, order_id, store):
    smtp_config = get_smtp_config()

    email = create_email(smtp_config, filename, order_id, store['name'])
    smtp_server = smtp_config['SERVER']['smtpServerURL']
    smtp_port = smtp_config['SERVER']['smtpServerPort']

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(
            smtp_config['USER']['smtpUserAddress'],
            smtp_config['USER']['smtpUserPassword']
        )
        server.send_message(email)


def get_smtp_config():
    smtp_config = configparser.ConfigParser()
    smtp_config.read('app/email_creds.cfg')

    return smtp_config


def create_email(smtp_config, filename, order_id, store_name):
    email = MIMEMultipart()
    subject = f"Order {order_id} - {store_name}"
    if 'test' in store_name.lower():
        subject = store_name

    email['Subject'] = subject
    email['From'] = smtp_config['USER']['smtpUserAddress']
    email['To'] = smtp_config['DEST']['destAddress']

    email.attach(create_order_attachment(filename))

    return email


def create_order_attachment(filename):
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)
    attachment = MIMEBase(maintype, subtype)

    with open(f"/tmp/{filename}", "rb") as order:
        attachment.set_payload(order.read())

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment",
                          filename=f"{str(datetime.now())}_order.xlsx")

    return attachment


def order_success(order_id):
    return {
        "status": "order successful",
        "id": order_id
    }


def order_failure(message):
    return {
        "status": "order failed",
        "message": message
    }
