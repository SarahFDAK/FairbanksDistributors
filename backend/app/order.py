import csv
from datetime import datetime, date, timedelta
import configparser
from flask import Blueprint, jsonify, request, url_for, redirect
import json
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import mimetypes

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

order = Blueprint('order', __name__)

@order.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


def order_success():
    return jsonify({"status": "order successful"})


@order.route('/place_order', methods=['POST', 'GET'])
def place_order():
    if request.method == 'POST':
        filename = f"{str(datetime.now())}_order.csv"
        filename = filename.replace(' ', '_')
        data = json.loads(request.form['order'])
        write_order_csv(data, filename)
        send_order(filename)
    else:
        write_order_csv({"store": "safeway", "order": {
                        "item": {"upc": "test", "amount": 0}}}, filename)
        send_order(filename)
    return order_success()


def is_next_week(delivery_date):
    today = date.today()
    return ((delivery_date - today) + timedelta(days=today.weekday())>=timedelta(days=7))


def format_date(date_iso):
    today = date.today()
    delivery_date = date(int(date_iso[0:4]),int(date_iso[5:7]), int(date_iso[8:10]))
    delivery_date_str = WEEKDAYS[delivery_date.weekday()]
    if is_next_week(delivery_date):
        delivery_date_str = f"{delivery_date_str} {date_iso[5:7]}/{date_iso[8:10]}"

    return delivery_date_str


def write_order_csv(order_info, filename):
    with open(f"/tmp/{filename}", "w") as order_file:
        order_writer = csv.writer(
            order_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        order_writer.writerow(['date'])
        date = format_date(order_info['date'])
        order_writer.writerow([date])

        order_writer.writerow(['store'])
        order_writer.writerow([order_info['store']])

        order_writer.writerow(['name', 'upc', 'amount'])
        order = order_info["items"]
        for item in order:
            order_writer.writerow([item['name'], item['upc'], item['amount']])


def send_order(filename):
    smtp_config = get_smtp_config()

    email = create_email(smtp_config, filename)

    with smtplib.SMTP_SSL(smtp_config['SERVER']['smtpServerURL'],
                          smtp_config['SERVER']['smtpServerPort']) as server:
        server.login(smtp_config['USER']['smtpUserAddress'],
                     smtp_config['USER']['smtpUserPassword'])
        server.send_message(email)


def get_smtp_config():
    smtp_config = configparser.ConfigParser()
    smtp_config.read('app/email_creds.cfg')
    return smtp_config


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
                          filename=f"{str(datetime.now())}_order.csv")

    return attachment


def create_email(smtp_config, filename):
    email = MIMEMultipart()
    email['Subject'] = 'An order'
    email['From'] = smtp_config['USER']['smtpUserAddress']
    email['To'] = smtp_config['DEST']['destAddress']

    email.attach(create_order_attachment(filename))

    return email
