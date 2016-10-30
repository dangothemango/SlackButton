# SlackButton
Configure an amazon IoT button to send messages to a slack channel

## Collabarators

Dan Gorman, Barbara Stall

# Setup and Configuration

## AWS Configuration

### updateTable Function

-Once in AWS select Lambda from the list of services
-Click 'Create Lambda Function'
-Select 'microservice-http-endpoint' from the list of templates
-Change Security to 'Open'
-Configure as shown, using the /updateTable/uploadThis.zip

![Update Table Setup Instructions](/pics/updateConfig.png)

### DynamoDB Table

### IOT Button and onPress Function

## Slack Custom Integrations

### Slash Command

### Incoming Webhook

- go to https://<your slack team>.slack.com/apps/build
- select Make a Custom Integration
- Select 'Incoming Webhooks'

![Alt](/wp.png "Title")
