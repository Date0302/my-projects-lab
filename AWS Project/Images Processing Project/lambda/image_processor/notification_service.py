import boto3

sns = boto3.client("sns")

def send_notification(topic_arn, message):

    sns.publish(
        TopicArn=topic_arn,
        Message=message
    )