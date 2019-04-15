from zabbix_api import ZabbixAPI
import time
import datetime
import boto3
from botocore.config import Config

# Integration with AWS
client = boto3.client(
    "sns",
    aws_access_key_id="Programmatic access key",
    aws_secret_access_key="Programmatic secret key",
    region_name="Region name for your sns",
    config=Config(proxies={'proxy address'}) # you can delete it if you won't use proxy
)

numbers = ["+48123123123"] # you can pass here every person who should get notifications
topic = client.create_topic(Name="Example") # if it doesn't created the topic will be created
topic_arn = topic['TopicArn'] # it simplifying getting arn 

# Caching function
def memoize(function):
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper


# Simple Contact Policy for notifications
def scheduler():
    date = datetime.datetime.now()
    if date.hour > 7 < 19:
        return True
    else:
        return False


# Function for sending messages (message:string, numbers:array, topic:topic, topic_arn:topic_arn)
@memoize
def send_message(message, numbers, topic, topic_arn):
    for number in numbers:
        client.subscribe(
            TopicArn=topic_arn,
            Protocol='sms',
            Endpoint=number  #  number who'll receive an SMS message.
        )
    client.publish(Message=message, TopicArn=topic_arn, MessageAttributes={
        'AWS.SNS.SMS.SenderID': {
            'DataType': 'String',
            'StringValue': 'Zabbix'
        }
    })

groups = ["some groups names"] # you can specify groups for filtraiting triggers

zapi = ZabbixAPI(server="https://zbxmain.example.com") # declare your zabbix address
zapi.login("username", "password") # basic authentication for zabbix frontend
print("Connected to Zabbix API Version %s" % zapi.api_version())


while True:
    if scheduler():
	for group in groups:
		triggers = zapi.trigger.get({
                "only_true": 1,
                "skipDependent": 1,
                "group": group,
                "monitored": 1,
                "active": 1,
                "output": "extend",
                "expandDescription": 1
                })
        	for t in triggers:
            		if int(t['value']) == 1:
                		send_message(t['description'], numbers, topic, topic_arn)
                		time.sleep(900)

