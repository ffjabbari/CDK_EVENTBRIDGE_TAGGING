import json
import boto3


def lambda_handler(event, context):
    print(event)
    # Extract the EC2 instance ID from the CloudWatch event
    instance_id = event['detail']['instance-id']

    # Create an SNS client
    sns_client = boto3.client('sns')

    # Define the SNS topic ARN
    sns_topic_arn = 'arn:aws:sns:us-east-1:981241700645:MySNSTopic'  # Replace with your SNS topic ARN

    # Create a message to publish to the SNS topic
    message = f"EC2 instance {instance_id} has been {event['detail']['state']}."

    # Publish the message to the SNS topic
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject=f"EC2 Instance {instance_id} {event['detail']['state']} Event"
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to SNS topic')
    }
