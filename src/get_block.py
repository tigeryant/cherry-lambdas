import paramiko
import os
import json
import boto3

# HOST = os.environ["NODE_IP"]
# USERNAME = os.environ["SSH_USER"]
# PASSWORD = os.environ["SSH_PASSWORD"]

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    parameter_names = ['NODE_IP', 'SSH_PASSWORD', 'SSH_USER']
    response = ssm.get_parameters(Names=parameter_names, WithDecryption=True)

    parameter_values = {}
    for parameter in response['Parameters']:
        parameter_values[parameter['Name']] = parameter['Value']

    HOST = parameter_values['NODE_IP']
    USERNAME = parameter_values['USERNAME']
    PASSWORD = parameter_values['PASSWORD']

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
    try:
        client.connect(HOST, username=USERNAME, password=PASSWORD, timeout=3)
    except:
        response_object['statusCode'] = 502
        response_object['body'] = json.dumps({"error": "failed to establish SSH connection"})
        return response_object
        
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
        response_object['body'] = json.dumps({"error": "lambda encountered an error"})
        
    return response_object
