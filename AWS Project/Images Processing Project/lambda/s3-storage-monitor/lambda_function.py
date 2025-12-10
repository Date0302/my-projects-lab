import boto3
import datetime

s3 = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')

bucket_name = 'my-image-processed-first'

def lambda_handler(event, context):
    print(" Metrics Lambda started")

    paginator = s3.get_paginator('list_objects_v2')
    total_size = 0
    total_objects = 0

    try:
        for page in paginator.paginate(Bucket=bucket_name, PaginationConfig={'PageSize': 100}):
            for obj in page.get('Contents', []):
                total_size += obj['Size']
                total_objects += 1

    except Exception as e:
        print(f" Error reading S3 bucket: {e}")
        raise e

    print(f" Total objects: {total_objects}")
    print(f" Total size: {total_size} bytes")

    try:
        cloudwatch.put_metric_data(
            Namespace='CustomS3',
            MetricData=[
                {
                    'MetricName': 'BucketSizeBytes',
                    'Timestamp': datetime.datetime.utcnow(),
                    'Value': total_size,
                    'Unit': 'Bytes'
                },
                {
                    'MetricName': 'NumberOfObjects',
                    'Timestamp': datetime.datetime.utcnow(),
                    'Value': total_objects,
                    'Unit': 'Count'
                }
            ]
        )
        print("✅ Metrics sent to CloudWatch")

    except Exception as e:
        print(f"❌ Error sending metrics: {e}")

    return {
        "status": "done",
        "objects": total_objects,
        "size": total_size
    }
