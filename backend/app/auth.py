import boto3
from flask import Flask, make_response, jsonify
import base64
from functools import wraps
from flask import session, g, request, redirect, url_for, make_response, jsonify
import json


def get_auth_key_from_aws():
    secret_name = "order_app/key"
    region_name = "us-west-2"
    auth_key = dict()

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(str(e))
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            auth_key = get_secret_value_response['SecretString']
        else:
            auth_key = base64.b64decode(
                get_secret_value_response['SecretBinary'])

        auth_key = (json.loads(auth_key))["order_app_key"]
        return auth_key


def authenticate(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        auth_key = get_auth_key_from_aws()
        user_auth_key = request.args.get("auth_key")

        if user_auth_key == auth_key:
            return function(*args, **kwargs)
        else:
            return make_response(jsonify({"Error": f"{user_auth_key} is not a valid authentication key"}), 401)

    return wrapped_function
