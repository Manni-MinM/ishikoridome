import pika

from config import Config


class RabbitMQClient:
    def __init__(self):
        creds = pika.PlainCredentials(Config.RBMQ_USER, Config.RBMQ_PASSWORD)
        connection_params = pika.ConnectionParameters(
            credentials=creds,
            host=Config.RBMQ_HOST,
            port=Config.RBMQ_PORT,
            virtual_host=Config.RBMQ_VIRTUAL_HOST,
            connection_attempts=Config.RBMQ_CONNECTION_RETRIES,
            retry_delay=Config.RBMQ_RETRY_DELAY_SECONDS,
            blocked_connection_timeout=Config.RBMQ_CONNECTION_TIMEOUT_SECONDS,
        )

        self.queue_name = Config.RBMQ_QUEUE_NAME
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def publish_message(self, national_id):
        message = {"national_id": national_id}
        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=str(message))

    def consume_messages(self, func):
        def callback(ch, method, properties, body):
            message = eval(body)
            national_id = message.get("national_id")
            func(national_id)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
