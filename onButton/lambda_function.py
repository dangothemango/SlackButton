import os
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import requests
import datetime
import json


ClickType={ 1 : 'SINGLE', 2 : 'DOUBLE', 3 : 'LONG'}
    
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    """Publishes a message to the configured Slack channel when and
    Amazon IoT button is pressed.
    Arguments:
      event (dict): Data passed to the handler by Amazon Lambda
      context (LambdaContext): Provides runtime information to the handler
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SlackButton')
    response=table.get_item(Key={
        'ButtonID': "HackMarist"
    })
   
    response=response['Item']
    print(response)
    
    slack_webhook_url = '<YourWebhookHere>'
        
    slack_message="No message found for click type"

    if event['clickType'] == ClickType[1]:
        if 'onPress' in response:
            slack_message=response["onPress"]

    if event['clickType'] == ClickType[2]:
        if 'onDoublePress' in response:
            slack_message=response["onDoublePress"]
        
    if event['clickType'] == ClickType[3]:
        if 'onLongPress' in response:
            slack_message=response["onLongPress"]
        
    result={
        'text': slack_message,
        'username': response["ButtonID"]
    }
    
    for i in ['icon_emoji','icon_url','channel']:
        if i in response:
            result[i]=response[i]
    if 'icon_url' in result and 'icon_emoji' in result:
        result.pop('icon_emoji',None)
    requests.post(slack_webhook_url, json=result)