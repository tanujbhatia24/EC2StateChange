import boto3
import json
import os

sns_client = boto3.client('sns')
TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    # Extract instance ID and state
    detail = event.get('detail', {})
    instance_id = detail.get('instance-id')
    state = detail.get('state')

    message = f"EC2 Instance {instance_id} is now {state.upper()}."
    subject = f"EC2 State Change: {state.upper()}"

    print(f"Sending notification: {message}")

    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject=subject
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }
