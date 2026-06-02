import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info("Workflow orchestration started")

    document_name = event.get("document_name", "unknown.txt")
    text = event.get("text", "")

    # Simulated document processing
    processed_document = {
        "document_name": document_name,
        "word_count": len(text.split())
    }

    logger.info("Document processing completed")

    # Simulated embedding generation
    embedding_result = {
        "embedding_status": "generated",
        "embedding_length": len(text)
    }

    logger.info("Embedding generation completed")

    final_response = {
        "document_processing": processed_document,
        "embedding_generation": embedding_result,
        "workflow_status": "completed"
    }

    logger.info("Workflow orchestration completed")

    return {
        "statusCode": 200,
        "body": json.dumps(final_response)
    }