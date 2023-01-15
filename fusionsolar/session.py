import logging
import os
import requests
import time
import functools

# Based on doucmentation iMaster NetEco V600R023C00 Northbound Interface Reference-V6(SmartPVMS)
# https://support.huawei.com/enterprise/en/doc/EDOC1100261860

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

user = 'robot_esl' #os.environ.get('FUSIONSOLAR_USER', 'unkown')
password = os.environ.get('FUSIONSOLAR_PASSWORD', 'unkown')


class Session:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password
        self.base_url = "https://eu5.fusionsolar.huawei.com/thirdData/"
        self.session = requests.session()
        self.session.headers.update(
            {'Connection': 'keep-alive', 'Content-Type': 'application/json'})
        self.token_expiration = 0

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def login(self) :
        '''Login to base url'''

        # Clears if already logged in
        self.session.cookies.clear()
        
        try:
            # Posts login request
            response = self._post(endpoint='login', json={'userName': user, 'systemCode': password})

            # Login succeeded, stores authentication token
            self.session.headers.update({'XSRF-TOKEN': response.cookies.get(name='XSRF-TOKEN')})

            # According to 7.1.1 The validity period of XSRF-TOKEN is 30 minutes.
            self.token_expiration = 30*60
        except Exception as e:
            logging.error(e)
            raise ValueError('Login failed. Invalid user or password.')

    def logout(self) :
        '''Logout to base url'''

    def succeeds(func):
        '''Ensures requests succeeds'''

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            self = args[0]
            try:
                response = func(*args, **kwargs)
                body = response.json()
                success = body.get('success', False)
                if success:
                    return body
                else:
                    raise Exception(body)
            except Exception as e:
                raise e
        return wrap
    
    @succeeds
    def _post(self, endpoint, json):
        '''Executes POST request'''
        try:
            response = requests.post(url=self.base_url + endpoint, json=json)
            response.raise_for_status()
        except Exception as e:
            # Forward all other exceptions/errors
            raise
        else:
            return response

"""
def connection_retry(func):
    '''Automatic retry on request timeout'''

    kMaxRetries = 2
    kRetryDelay = 1

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        i = 0
        while True:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectTimeout as e:
                logging.info(e)
                if i >= self.kMaxRetries :
                    logging.error('Max retries exceeded.')
                    raise e

                # Will retry
                i += 1
                time.sleep(self.kRetryDelay)
                continue
    return wrapper
"""