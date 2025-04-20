import os, boto3, io, uuid
from PIL import Image

s3 = boto3.client("s3")

RAW_BUCKET   = os.environ["RAW_BUCKET"]
THUMB_BUCKET = os.environ["THUMB_BUCKET"]   # make sure template uses this

def lambda_handler(event, context):
    print("Trigger:", event)

    for record in event["Records"]:
        key = record["s3"]["object"]["key"]
        print("Raw key:", key)

        # 1. download original
        obj = s3.get_object(Bucket=RAW_BUCKET, Key=key)
        image_data = obj["Body"].read()

        # 2. resize
        img = Image.open(io.BytesIO(image_data))
        img.thumbnail((300, 300))

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        buf.seek(0)

        # 3. upload thumbnail
        thumb_key = f"thumb-{uuid.uuid4()}.jpg"
        s3.put_object(
            Bucket=THUMB_BUCKET,
            Key=thumb_key,
            Body=buf,
            ContentType="image/jpeg",
        )

        print(f"Thumbnail saved to {THUMB_BUCKET}/{thumb_key}")
