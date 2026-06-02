import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info("Document processing started")

    document_name = event.get("document_name", "unknown.txt")
    content = event.get("content", "")

    word_count = len(content.split())

    logger.info(f"Processed document: {document_name}")
    logger.info(f"Word count: {word_count}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "document_name": document_name,
            "word_count": word_count,
            "message": "Document processed successfully"
        })
    }