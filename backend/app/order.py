from .auth import authenticate

import csv
import pathlib as pl
from datetime import datetime, date, timedelta
import configparser
import json
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from .write_order_xlsx import write_xlsx
import mimetypes

from flask import Blueprint, jsonify, request, url_for, redirect, make_response
import boto3

order = Blueprint('order', __name__)


@order.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


@order.route('/login')
@authenticate
def login():
    return make_response(jsonify({"Success": "Authentication code is valid"}), 200)


@order.route('/items/chips', methods=['GET'])
@authenticate
def get_chips(): 
    return get_bucket_data('chips.json')


@order.route('/items/freezer_bread', methods=['GET'])
@authenticate
def get_freeze_bread(): 
    return get_bucket_data('freezer_bread.json')


def get_bucket_data(key):
    BUCKET_NAME = 'fd-order-app-storage'

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    download_path = pl.Path('/') / 'tmp' / key
    bucket.download_file(key, str(download_path))

    with download_path.open('r') as f:
        items = json.load(f)

    return jsonify(items)


def order_success():
    return jsonify({"status": "order successful"})


def order_failure(message):
    return jsonify({"status": "order failed",
                    "message": message})


@order.route('/place_order', methods=['POST', 'GET'])
@authenticate
def place_order():
    filename = f"{str(datetime.now())}_order.xlsx"
    filename = filename.replace(' ', '_')
    if request.method == 'POST':
        try:
            data = json.loads(request.form['order'])
            write_xlsx(f"/tmp/{filename}",data)
            send_order(filename, data['store'])
        except Exception as e:
            return order_failure(str(e))
    else:
        write_xlsx(f"/tmp/{filename}",{"date": "2002-02-02", "store": "safeway",
                         "items": [{"name": "chip", "upc": "test", "amount": 0}]})
        send_order(filename, "safeway")
    return order_success()

def send_order(filename, store_name):
    smtp_config = get_smtp_config()

    email = create_email(smtp_config, filename, store_name)

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
                          filename=f"{str(datetime.now())}_order.xlsx")

    return attachment


def create_email(smtp_config, filename, store_name):
    email = MIMEMultipart()
    email['Subject'] = store_name
    email['From'] = smtp_config['USER']['smtpUserAddress']
    email['To'] = smtp_config['DEST']['destAddress']

    email.attach(create_order_attachment(filename))

    return email
