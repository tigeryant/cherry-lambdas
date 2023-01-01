import paramiko
import os
import json

HOST = os.environ["NODE_IP"]
USERNAME = os.environ["SSH_USER"]
PASSWORD = os.environ["SSH_PASSWORD"]

def lambda_handler(event, context):
    response_object = {}
    response_object['headers'] = {}
    response_object['headers']['Content-type'] = 'application/json'
    
    if 'hash' in event['queryStringParameters']:
        if event['queryStringParameters']['hash'] != "":
            input_hash = event['queryStringParameters']['hash']
        else:
            response_object['statusCode'] = 400
            response_object['body'] = json.dumps({"error": "hash parameter value was missing from request"})
            return response_object
    else:
        response_object['statusCode'] = 422
        response_object['body'] = json.dumps({"error": "hash parameter key was missing from request"})
        return response_object
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USERNAME, password=PASSWORD)
    _stdin, _stdout, _stderr = client.exec_command(f"bitcoin-cli -named getblock blockhash={input_hash} verbosity=1")
    response = _stdout.read().decode().strip()
    error = _stderr.read().decode().strip()
    client.close()
    
    if response:
        response_object['statusCode'] = 200
        response_object['body'] = response
    elif error:
        response_object['statusCode'] = 502
        response_object['body'] = error
    else:
        response_object['statusCode'] = 500
        response_object['body'] = json.dumps({"message": "custom message - lambda encountered an error"})
        
    return response_object
