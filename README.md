# SlackButton
Configure an amazon IoT button to send messages to a slack channel

## Collabarators

Dan Gorman, Barbara Stall

# Setup and Configuration

## AWS Configuration

### updateTable Function

* Once in AWS select Lambda from the list of services
* Click 'Create Lambda Function'
* Select 'microservice-http-endpoint' from the list of templates
* Change Security to 'Open'
* Configure as shown, using the /updateTable/uploadThis.zip fill out your role name using something like "SlackButton" remember this for later

![Update Table Setup Instructions](/pics/updateConfig.png)

* Finish the setup until you see this screen

![APIURL](/pics/APIURL.png)

* Copy that URL you'll need it for later

### DynamoDB Table

* Once in AWS select DynamoDB from the list of services
* Click table
* Configure as shown

![Table Config](/pics/createTable.png)

### IOT Button and onPress Function

* Once in AWS select Lambda from the list of services
* Click 'Create Lambda Function'
* Search for and select the IoT template
* Follow the prompts to setup the IoT button
* Configure the function as shown below
* The most important thing here is to make sure the role is the same role you made in the updateTable function
* Use /onPress/uploadThis.zip
* Once the code has been uploaded, you must change line 33 to the name of the button you will use, any character except spaces and 39 to your webhook url which we havent created

![On Press Setup Instructions](/pics/onPressConfig.png)

## Slack Custom Integrations

### Incoming Webhook

* go to https://<your slack team>.slack.com/apps/build
* select Make a Custom Integration
* Select 'Incoming Webhooks'
* Configure this any way yould like too and then copy the webhook URL into line 39 of your onButton Function

### Slash Command

* go to https://<your slack team>.slack.com/apps/build
* select Make a Custom Integration
* Select 'Slash Command'
* The only important configurations here are the URL box must be the API URL we saved from the updateTable function, and it must be a POST method
* For the purposes of the tutorial, we will assume the command chosen was /button

![Slash Command Config](/pics/slashCmd.png)

# Usage

![Sample Usage](/pics/sampleCommand.png)

* The only required argument is Button name, the rest are optional as follows
* -p: The message you want to display on a single press
* -d: The message you want to display on a double press
* -l: The message you want to display on a long press
* -e: The slack emoji you would like to display as the buttons photo
* -u: Alternately a url to the icon you would like to use as the photo
* -c: the default channel is the one active when the command is sent, use -c to overwrite
* Url responses and direction for AWS is handled automatically
