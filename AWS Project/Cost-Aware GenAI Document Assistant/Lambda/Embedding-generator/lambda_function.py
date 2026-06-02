import json
import logging
import hashlib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_fake_embedding(text):

    hash_object = hashlib.md5(text.encode())
    embedding = hash_object.hexdigest()

    return embedding

def lambda_handler(event, context):

    logger.info("Embedding generation started")

    text = event.get("text", "")

    embedding = generate_fake_embedding(text)

    logger.info("Embedding generated successfully")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": text,
            "embedding": embedding,
            "message": "Embedding generated successfully"
        })
    }