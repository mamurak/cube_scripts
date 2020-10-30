import logging
import argparse

import pika


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    return args


def test_connection(host_or_ip, port=5672):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        host_or_ip, credentials=credentials, port=port
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(
        exchange='test_exchange',
        exchange_type='direct',
        passive=False,
        durable=True,
        auto_delete=False)

    log.info('Sending message to create a queue')
    channel.basic_publish(
        'test_exchange', 'standard_key', 'queue:group',
        pika.BasicProperties(content_type='text/plain', delivery_mode=1))

    connection.sleep(5)

    log.info('Sending text message to group')
    channel.basic_publish(
        'test_exchange', 'group_key', 'Message to group_key',
        pika.BasicProperties(content_type='text/plain', delivery_mode=1))

    connection.sleep(5)

    log.info('Sending text message')
    channel.basic_publish(
        'test_exchange', 'standard_key', 'Message to standard_key',
        pika.BasicProperties(content_type='text/plain', delivery_mode=1))

    connection.close()

    log.info('Done.')


def main():
    args = get_args()
    ip = args.ip_address
    port = args.port
    test_connection(ip, port=port)


if __name__ == '__main__':
    main()
