import logging
import argparse

from requests import post, Session


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def main():
    log.info('Starting Chris test.')
    arguments = read_arguments()
    host = arguments.host
    port = arguments.port
    user_name = arguments.user
    password = arguments.password
    endpoint = get_endpoint(host, port)
    create_user(endpoint, user_name, password)
    do_test_request(endpoint, user_name, password)
    log.info('Done.')


def read_arguments():
    log.debug('Reading arguments.')
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('--port', type=int)
    parser.add_argument('--user', default='test-user')
    parser.add_argument('--password', default='test1234')
    arguments = parser.parse_args()
    return arguments


def get_endpoint(host, port):
    log.debug(f'Creating URL from host {host} and port {port}.')
    return f'http://{host}:{port}/api/v1/'


def create_user(endpoint, user_name, password):
    log.info(
        f'Creating user {user_name} with password {password} through {endpoint}.'
    )
    headers = {
        'Content-Type': 'application/vnd.collection+json',
        'Accept': 'application/vnd.collection+json',
    }
    request_body = {
        'template': {
            'data': [
                {'name': 'username', 'value': user_name},
                {'name': 'password', 'value': password},
                {'name': 'email', 'value': 'test@gmail.com'}
            ]
        }
    }
    url = f'{endpoint}users/'
    log.debug(f'Sending request to {url} with content: {request_body}.')
    response = post(url, json=request_body, headers=headers)
    log.info(f'Received response with status code {response.status_code}.')
    log.debug(f'Response content: {response.content}.')
    return response


def do_test_request(endpoint, user_name, password):
    log.info(
        f'Executing test request against {endpoint}' 
        f'with user {user_name} and password {password}.'
    )
    with Session() as session:
        session.auth = user_name, password
        response = session.get(endpoint)
    log.info(f'Received response with status code {response.status_code}.')
    log.debug(f'Response content: {response.content}.')
    return response


if __name__ == '__main__':
    main()