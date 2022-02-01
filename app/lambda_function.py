import json
import boto3
import urllib.parse
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    print(bucket)
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # key = 'input/' + key
    key = key
    print(key)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response["Body"]
        # print("CONTENT TYPE: " + response['ContentType'])
        content_data = content.read().decode()
        print(content_data)
        # return content.read().decode()
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    # print("Event --", event['body'])
    # event_body = json.loads(event['body'])
    # print("type of event body::", type(event_body))
    # This address must be verified with Amazon SES.
    SENDER = "something@gmail.com"

    # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = "something@gmail.com"

    # the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "mysubject"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 )

    # The HTML body of the email.
    BODY_HTML = content_data

    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create SES client
    ses = boto3.client('ses', region_name=AWS_REGION)
    try:
        # Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    # else:
    #     print("Email sent! Message ID:"),
    #     print(response['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')}
