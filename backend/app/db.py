import base64
import json

import psycopg2
import boto3
from botocore.exceptions import ClientError

import json
from contextlib import contextmanager


def db_config():
    secret_name = "fd-orders-db-config"
    region_name = "us-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        config = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print('Error loading db creds: ', e)
        raise e

    return json.loads(config['SecretString'])


CONFIG = db_config()


@contextmanager
def connect():
    yield psycopg2.connect(
        user=CONFIG['user'],
        password=CONFIG['pass'],
        host=CONFIG['host'],
        port=CONFIG['port'],
        database=CONFIG['database']
    )
