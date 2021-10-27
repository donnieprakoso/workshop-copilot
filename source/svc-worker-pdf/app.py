import boto3
import os
import errno
from datetime import datetime
import logging
import boto3
import os
from botocore.exceptions import ClientError
import json
import pdfkit
import requests

AWS_REGION = os.getenv("AWS_REGION")
SQS_URI = os.getenv("COPILOT_QUEUE_URI")
S3_BUCKET = os.getenv("S3PDFREQUESTS_NAME")
SVC_API_ENDPOINT = os.getenv("SVC_API_ENDPOINT")
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

sqs_client = boto3.client("sqs", region_name=AWS_REGION)

def create_directory(path):
    try:
        os.makedirs(path)
        return True
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return False
        else:
            return False


def update_request_status(data):
    logger.info(
        "Sending update to svc-api endpoint {} with data: {}".format(SVC_API_ENDPOINT, data))
    req = requests.post("{}/status".format(SVC_API_ENDPOINT), json=data)


def upload_to_s3(filepath):
    filename = os.path.basename(filepath)
    bucket = S3_BUCKET
    key = os.path.join("/", filename)

    args = {'ServerSideEncryption': 'AES256'}
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    s3_resp = s3_client.upload_file(filepath, bucket, key, ExtraArgs=args)
    logger.info(s3_resp)
    url = s3_client.generate_presigned_url('get_object', ExpiresIn=3600, Params={'Bucket': bucket, 'Key': key})
    return url


def receive_queue_message():
    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_URI, WaitTimeSeconds=5, MaxNumberOfMessages=1)
    except ClientError:
        logger.exception('Could not receive the message from the - {}.'.format(
            SQS_URI))
        raise
    else:
        return response


def delete_queue_message(receipt_handle):
    try:
        response = sqs_client.delete_message(QueueUrl=SQS_URI,
                                             ReceiptHandle=receipt_handle)
    except ClientError:
        logger.exception('Could not delete the meessage from the - {}.'.format(
            SQS_URI))
        raise
    else:
        return response


if __name__ == '__main__':
    while True:
        messages = receive_queue_message()
        if "Messages" in messages:
            for msg in messages['Messages']:
                try:
                    receipt_handle = msg['ReceiptHandle']
                    message = json.loads(msg['Body'])
                    payload = json.loads(message["Message"])["payload"]
                    data = {}
                    data['request_ID'] = payload['request_ID']
                    data['request_url'] = payload['request_url']

                    create_directory("/tmp/images/requests/")
                    fileoutput_path = "/tmp/images/requests/{}.pdf".format(
                        data['request_ID'])
                    pdfkit.from_url(data['request_url'], fileoutput_path)
                    data["request_output"] = upload_to_s3(fileoutput_path)
                    data["request_status"] = "Completed"
                    data["request_completed"] = True
                    update_request_status(data)
                except:
                    logger.exception(
                        "Problem on processing request {}. Latest data {}".format(data["request_ID"], data))
                    data["request_status"] = "Error"
                    data["request_completed"] = False
                    update_request_status(data)
                finally:
                    logger.info('Deleting message from the queue...')
                    resp_delete = delete_queue_message(receipt_handle)
                logger.info(
                    'Received and deleted message(s) from {} with message {}.'.format(SQS_URI, resp_delete))
