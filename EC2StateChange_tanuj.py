import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    try:
        instance_id = event['detail']['instance-id']
    except KeyError:
        print("No instance ID found in the event.")
        return {'statusCode': 400, 'body': 'Instance ID not found'}

    # Get user/role who launched the instance (from CloudTrail event details)
    user = "Unknown"
    try:
        user = event['detail']['userIdentity']['arn']
    except KeyError:
        print("Could not extract user identity from event.")
    
    # Define tags
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    tags = [
        {'Key': 'LaunchDate', 'Value': current_date},
        {'Key': 'LaunchedBy', 'Value': user}
    ]

    # Apply tags
    try:
        ec2.create_tags(Resources=[instance_id], Tags=tags)
        print(f"Successfully tagged instance {instance_id} with tags: {tags}")
        return {'statusCode': 200, 'body': f'Tagged instance {instance_id}'}
    except Exception as e:
        print(f"Failed to tag instance: {str(e)}")
        return {'statusCode': 500, 'body': 'Error tagging instance'}
