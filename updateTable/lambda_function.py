from __future__ import print_function

import boto3
import json
import urllib

result={}

arg2key={
	"c" :"channel",
	"e" :"icon_emoji",
	"u" :"icon_url",
	"p" :"onPress",
	"d" :"onDoublePress",
	"l" :"onLongPress"
}

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))
   
    operations = {
        'POST': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if not operation in operations:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
    payload = event['body'].split("&")
    for item in payload:
        if item.startswith("text="):
            data=parse(urllib.unquote(item[5:]).decode('utf8'))
            if not data:
                return respond(ValueError("No Button Name Specified"))
        elif item.startswith("response_url="):
            rURL=urllib.unquote(item[13:]).decode('utf8')
    data["Item"]['URL']=rURL
    dynamo = boto3.resource('dynamodb').Table("SlackButton")
    try:
        dynamo.update_item(**data)
    except:
        dynamo.put_item(**data)
    return respond(None, "Update Succesful")
        
def parse(argv):
    argv=argv.replace("+", ' ')
    argv = argv.split(' ',1)
    
    if len(argv) <1:
        return False
    result['ButtonID'] = argv[0]
    if len(argv) > 1:
        args = argv[1]
        args=args.split('-')
        
        for arg in args:
        	if len(arg)==0:
        		continue
        	arg=arg.strip().split(' ',1)
        	key=arg2key[arg[0].lower()]
        	result[key]=arg[1]
    return { "Item": result }
