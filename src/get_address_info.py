import paramiko
import os
import json

HOST = os.environ["NODE_IP"]
USERNAME = os.environ["SSH_USER"]
PASSWORD = os.environ["SSH_PASSWORD"]

def lambda_handler(event, context): 
    address = event['queryStringParameters']['address']
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USERNAME, password=PASSWORD)
    _stdin, _stdout, _stderr = client.exec_command(f"bitcoin-cli getaddressinfo {address}")
    response = _stdout.read().decode()
    client.close()
    
    response_object = {}
    response_object['statusCode'] = 200
    response_object['headers'] = {}
    response_object['headers']['Content-type'] = 'application/json'
    response_object['body'] = json.dumps(response)
    
    return response_object
