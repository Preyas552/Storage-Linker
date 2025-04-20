import os, json, boto3, uuid

s3 = boto3.client('s3')
RAW = os.environ['RAW_BUCKET']

def lambda_handler(event, context):
    key = f"{uuid.uuid4()}.jpg"
    url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': RAW, 'Key': key, 'ContentType': 'image/jpeg'},
        ExpiresIn=900
    )
    return {
        "statusCode": 200,
        "body": json.dumps({"uploadUrl": url, "key": key})
    }
