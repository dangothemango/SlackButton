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
    print("!")
    dynamodb = boto3.resource('dynamodb')
    print("2")
    table = dynamodb.Table('SlackButton')
    print ("3")
    response=table.get_item(Key={
        'ButtonID': "NewButton"
    })
    # {u'username': u'BeckyButton', 
    # u'onLongPress': u'Walked and Fed', u'onDoublePress': u'Fed', 
    # u'URL': u'https://hooks.slack.com/services/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', 
    # u'ButtonID': u'Becky', u'icon_emoji': u':dog:', u'Channel': u'#hackmarist', u'onPress': u'Walked'}
    response=response['Item']
    print(response)
    
    slack_webhook_url = "https://hooks.slack.com/services/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"
    if "channel" in response:
        slack_channel = response["channel"]
        
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
        'channel': slack_channel,
        'username': response["ButtonID"]
    }
    
    for i in ['icon_emoji','icon_url']:
        if i in response:
            result[i]=response[i]
        
    requests.post(slack_webhook_url, json=result)