import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

def save_metadata(table_name, image_id, original_key, thumbnail_key):

    table = dynamodb.Table(table_name)

    table.put_item(
        Item={
            "imageId": image_id,
            "originalKey": original_key,
            "thumbnailKey": thumbnail_key,
            "status": "PROCESSED",
            "processedAt": datetime.utcnow().isoformat()
        }
    )