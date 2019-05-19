import boto3


# assumes one line per file containing only the api key
def get_api_key_from_s3(bucket='segmental', key_file='api_key.txt'):
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket, key_file)
    key = obj.get()['Body'].read().decode('utf-8')

    return key
