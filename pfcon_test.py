import logging
import argparse

from requests import post


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def main():
    log.info('Starting pfcon test.')
    arguments = get_arguments()
    host = arguments.host
    port = arguments.port
    do_request(host, port)
    log.info('Done.')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    arguments = parser.parse_args()
    return arguments


def do_request(host, port=5005):
    url = f'http://{host}:{port}/api/v1/cmd'
    log.info(f'Requesting pfcon through {url}.')

    request_body = {
        'payload': {
            'action': 'hello',
            'meta': {
                'askAbout': 'sysinfo', 'echoBack': 'Hi there!', 'service': 'host'
            }
        }
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = post(url, json=request_body, headers=headers)

    log.info(f'Received response with status code {response.status_code}')
    log.debug(f'Response content: {response.content}')


if __name__ == '__main__':
    main()
