import boto3


def get_api_key_from_s3(bucket='segmental', key='api_key.txt'):
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket, key)
    key = obj.get()['Body'].read().decode('utf-8')

    return key
