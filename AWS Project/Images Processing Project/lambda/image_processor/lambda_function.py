import json
import os
import logging

from image_service import create_thumbnail
from storage_service import download_file, upload_file
from metadata_service import save_metadata
from notification_service import send_notification


# 环境变量读取（生产级标准）
TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


# 设置日志（CloudWatch最佳实践）
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info("Lambda invoked")
    logger.info(f"Received event: {json.dumps(event)}")

    results = []

    for record in event.get("Records", []):

        try:

            body = json.loads(record["body"])

            image_id = body["imageId"]
            original_key = body["originalKey"]

            logger.info(f"Processing image_id: {image_id}")
            logger.info(f"Original key: {original_key}")

            input_path = f"/tmp/{image_id}"
            output_path = f"/tmp/thumb-{image_id}"

            # Step 1: 下载原始图片
            download_file(BUCKET_NAME, original_key, input_path)
            logger.info("Download completed")

            # Step 2: 创建缩略图
            create_thumbnail(input_path, output_path)
            logger.info("Thumbnail created")

            # Step 3: 上传缩略图
            thumbnail_key = f"thumb-{original_key}"
            upload_file(output_path, BUCKET_NAME, thumbnail_key)
            logger.info(f"Thumbnail uploaded: {thumbnail_key}")

            # Step 4: 保存metadata
            save_metadata(
                TABLE_NAME,
                image_id,
                original_key,
                thumbnail_key
            )
            logger.info("Metadata saved")

            # Step 5: 发送通知
            send_notification(
                SNS_TOPIC_ARN,
                f"Image processed successfully: {image_id}"
            )
            logger.info("Notification sent")

            results.append({
                "imageId": image_id,
                "status": "SUCCESS"
            })

        except Exception as e:

            logger.error(f"Error processing image: {str(e)}")

            results.append({
                "imageId": body.get("imageId", "UNKNOWN"),
                "status": "FAILED",
                "error": str(e)
            })

            # 重新抛出异常，让SQS触发重试机制
            raise e

    logger.info("Lambda execution completed")

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }