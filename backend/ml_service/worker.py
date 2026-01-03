import os
import json
import logging
import pika
from ml import classify_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBIT_HOST = os.getenv("RABBIT_HOST", "queue")
QUEUE_NAME = os.getenv("ML_QUEUE", "sentiment")

def ensure_connection() -> pika.BlockingConnection:
    """Establish connection to RabbitMQ with retries."""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    connection_attempts=3,
                    retry_delay=2
                )
            )
            logger.info("Connected to RabbitMQ")
            return connection
        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                import time
                time.sleep(retry_delay)
            else:
                raise

def process_message(ch, method, properties, body):
    """Process incoming sentiment analysis request."""
    try:
        message = json.loads(body)
        text = message.get("text")
        request_id = message.get("request_id")
        
        if not text:
            logger.error(f"Request {request_id}: No text provided")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        logger.info(f"Processing request {request_id}: analyzing text")
        result = classify_text(text)
        
        # Extract the label with highest score
        label = max(result[0], key=lambda d: d["score"])["label"]
        sentiment = f"The sentiment of this text is {label}."
        
        logger.info(f"Request {request_id}: sentiment = {label}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """Start the ML worker service."""
    logger.info("Starting ML worker service")
    
    import os
    import json
    import logging
    import pika
    from ml import classify_text

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    RABBIT_HOST = os.getenv("RABBIT_HOST", "queue")
    QUEUE_NAME = os.getenv("ML_QUEUE", "sentiment")

    def ensure_connection() -> pika.BlockingConnection:
        """Establish connection to RabbitMQ with retries."""
        max_retries = 5
        retry_delay = 2
    
        for attempt in range(max_retries):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBIT_HOST,
                        connection_attempts=3,
                        retry_delay=2
                    )
                )
                logger.info("Connected to RabbitMQ")
                return connection
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                else:
                    raise

    def process_message(ch, method, properties, body):
        """Process incoming sentiment analysis request."""
        try:
            message = json.loads(body)
            text = message.get("text")
            request_id = message.get("request_id")
        
            if not text:
                logger.error(f"Request {request_id}: No text provided")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
        
            logger.info(f"Processing request {request_id}: analyzing text")
            result = classify_text(text)
        
            # Extract the label with highest score
            label = max(result[0], key=lambda d: d["score"])["label"]
            sentiment = f"The sentiment of this text is {label}."
        
            logger.info(f"Request {request_id}: sentiment = {label}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def main():
        """Start the ML worker service."""
        logger.info("Starting ML worker service")
    
        connection = ensure_connection()
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)
    
        logger.info(f"Listening for messages on queue '{QUEUE_NAME}'")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Shutting down ML worker")
            channel.stop_consuming()
            connection.close()

    if __name__ == "__main__":
        main()
