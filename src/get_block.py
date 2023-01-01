import paramiko
import os
import json

HOST = os.environ["NODE_IP"]
USERNAME = os.environ["SSH_USER"]
PASSWORD = os.environ["SSH_PASSWORD"]

def lambda_handler(event, context): 
    input_hash = event['queryStringParameters']['hash']
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USERNAME, password=PASSWORD)
    _stdin, _stdout, _stderr = client.exec_command(f"bitcoin-cli -named getblock blockhash={input_hash} verbosity=1")
    response = _stdout.read().decode().strip()
    error = _stderr.read().decode().strip()
    client.close()
    
    response_object = {}
    response_object['headers'] = {}
    response_object['headers']['Content-type'] = 'application/json'
    
    if response:
        response_object['statusCode'] = 200
        response_object['body'] = response
    elif error:
        response_object['statusCode'] = 502
        response_object['body'] = error
    else:
        response_object['statusCode'] = 500
        response_object['body'] = json.dumps({"Message": "Custom message - lambda failed"})
        
    return response_object
