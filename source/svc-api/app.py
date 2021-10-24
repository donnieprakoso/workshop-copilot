import os
import json
import boto3
import sys
import traceback
import uuid
import os
from datetime import datetime
from flask import Flask
from flask import request as _request
from flask import jsonify
import logging
import time

app = Flask(__name__)

SNS_ARN = json.loads(os.getenv('COPILOT_SNS_TOPIC_ARNS'))
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE = os.getenv("PDFREQUESTS_NAME")
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def save_request_received(data):
    dynamodb_table = dynamodb.Table(DYNAMODB_TABLE)
    response = dynamodb_table.update_item(
        Key={'REQUEST_ID': data['request_ID']},
        UpdateExpression="set request_status=:request_status, request_url=:request_url, request_completed=:request_completed, request_timestamp=:request_timestamp",
        ExpressionAttributeValues={
            ':request_status': "Received",
            ':request_url': data['request_url'],
            ':request_completed': False,
            ':request_timestamp': data['request_timestamp']
        })


def save_request_status(data):
    dynamodb_table = dynamodb.Table(DYNAMODB_TABLE)
    response = dynamodb_table.update_item(
        Key={'REQUEST_ID': data['request_ID']},
        UpdateExpression="set request_status=:request_status, request_completed=:request_completed, request_output=:request_output",
        ExpressionAttributeValues={
            ':request_status': data["request_status"],
            ':request_completed': data["request_completed"],
            ':request_output': data["request_output"]
        })


def get_data(id):
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.get_item(
        Key={
            'REQUEST_ID': id
        }
    )
    logger.info("Item {}".format(response))
    item = response['Item']
    return item


@app.route('/ping', methods=['GET'])
def ping():
    try:
        return jsonify({"value": "ok"}), 200
    except:
        logging.exception(exc_info=True)
        traceback.print_exc(file=sys.stdout)
        return jsonify({"error": "error"}), 500


@app.route('/status/<request_id>', methods=['GET'])
def status(request_id):
    try:
        logger.info("ID : {}".format(request_id))
        data = get_data(request_id)
        logger.info("DATA {}".format(data))

        if data['request_completed']:
            response = {"ID": data['REQUEST_ID'],
                        "URL": data['request_output'],
                        "request_status": data['request_status'],
                        "request_completed": data['request_completed']}
            return jsonify(response), 200
        else:
            response = {
                "request_status": data['request_status'], "request_completed": data['request_completed']}
            return jsonify(response), 204

    except:
        logger.exception("Error on getting status for request_ID: {}".format(
            request_id), exc_info=True)
        return jsonify({"error": "error"}), 500


@app.route('/status', methods=['POST'])
def status_process():
    req = _request.get_json()
    try:
        if not req["request_ID"]:
            return jsonify({"error": "Parameters missing"}), 422
        data = {}
        data["request_ID"] = req["request_ID"]
        data["request_url"] = req["request_url"]
        data["request_status"] = req["request_status"]
        data["request_completed"] = req["request_completed"]
        data["request_output"] = req["request_output"] if "request_output" in req else ""
        save_request_status(data)
        return jsonify({"status": "ok"}), 200
    except:
        logger.exception("Error on updating status", exc_info=True)
        return jsonify({"error": "error"}), 500


@app.route('/process', methods=['POST'])
def process():
    req = _request.get_json()
    logger.info(req)
    try:
        if "request_url" not in req:
            return jsonify({"error": "Parameters missing"}), 422

        if not req["request_url"]:
            return jsonify({"error": "Parameters missing"}), 422

        request_id = str(uuid.uuid4())
        data = {"request_ID": request_id, "request_url": req["request_url"], "request_timestamp": time.strftime(
            "%Y-%m-%dT%H:%M:%S", time.localtime())}
        save_request_received(data)
        resp_sns = sns_client.publish(
            TopicArn=SNS_ARN["requests"],
            Message=json.dumps(
                {"payload": {"request_ID": request_id, "request_url": req["request_url"]}}))
        logger.info(resp_sns)
        return jsonify({"request_ID": request_id}), 200

    except:
        logger.exception("Error on processing request", exc_info=True)
        return jsonify({"error": "error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
