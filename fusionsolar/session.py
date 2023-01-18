import logging
import os
import requests
import json
import functools

# Based on documentation iMaster NetEco V600R023C00 Northbound Interface Reference-V6(SmartPVMS)
# https://support.huawei.com/enterprise/en/doc/EDOC1100261860


# Public API exception

class FusionException(Exception):
    '''Undefined Fusion exception'''


class FusionPublicException(FusionException):
    '''Undefined public fusion exception'''


class LoginFailed(FusionPublicException):
    '''Login failed. Verify user and password of Northbound API account.'''


class FrequencyLimit(FusionPublicException):
    '''(407) The interface access frequency is too high.'''

# TODO    401 You do not have the related data interface permission.


# Internal exceptions, should not get out of module implementation

class _FusionInternalException(FusionException):
    '''Undefined internal fusion exception'''


class _305_NotLogged(_FusionInternalException):
    '''You are not in the login state. You need to log in again.'''


def FailCodeToException(body):
    switcher = {
        305: _305_NotLogged,  # You are not in the login state.
        407: FrequencyLimit,  # The interface access frequency is too high.
        20001: LoginFailed,  # The third-party system ID does not exist.
        20002: LoginFailed,  # The third-party system is forbidden.
        20003: LoginFailed,  # The third-party system has expired.
        30029: LoginFailed,  # Authentication failed.
    }

    # Returns the exception matching failCode, or FusionException by default
    failCode = body.get('failCode', 0)
    logging.debug('failCode ' + str(failCode) + ' received.')
    return switcher.get(failCode, _FusionInternalException)(body)


def logged(func):
    '''Ensures user is logged, login again if necessary'''

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        login_again = False
        while True:
            if (login_again):
                args[0].login()
            try:
                return func(*args, **kwargs)
            except _305_NotLogged:
                login_again = True

    return wrap


def validate(func):
    '''Ensures requests succeeds'''

    @functools.wraps(func)
    def wrap(*args, **kwargs) -> tuple[requests.Response, dict]:
        response = func(*args, **kwargs)
        body = response.json()
        if not body.get('success', False):
            raise FailCodeToException(body)
        return response, body
    return wrap


def exceptions_sanity(func):
    '''Ensures sanity of exceptions raised to the public API. No internal exception should get to public side.'''

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except _FusionInternalException as e:
            logging.exception()
            raise FusionException()

    return wrap


class Session:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password
        self.base_url = "https://eu5.fusionsolar.huawei.com/thirdData/"
        self.session = requests.session()
        self.session.headers.update(
            {'Connection': 'keep-alive', 'Content-Type': 'application/json'})

    @exceptions_sanity
    def __enter__(self):
        self.login()
        return self

    @exceptions_sanity
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    @exceptions_sanity
    def logout(self) -> None:
        '''Logout from base url'''
        self.session = requests.session()

    @exceptions_sanity
    def login(self) -> None:
        '''Login to base url'''

        try:
            # Posts login request
            self.session.cookies.clear()
            response, body = self._raw_post(endpoint='login', json={
                'userName': self.user, 'systemCode': self.password})
            # Login succeeded, stores authentication token
            self.session.headers.update(
                {'XSRF-TOKEN': response.cookies.get(name='XSRF-TOKEN')})
        except _305_NotLogged:
            # Login failed can also be raised directly for 20001, 20002, 20003 failCodes.
            raise LoginFailed() from None
        except json.JSONDecodeError:
            # FusionSolar NBI sends an empty json when user is unknown. It's not the expected behavior described by documentation 7.1.1.
            # It's caught here with JSONDecodeError exception.
            raise LoginFailed() from None

    @exceptions_sanity  # Must be the first decorator.
    @logged
    def post(self, endpoint, json={}) -> None:
        '''Executes POST request'''
        return self._raw_post(endpoint, json)

    @validate
    def _raw_post(self, endpoint, json={}) -> requests.Response:
        '''Executes POST request'''
        try:
            response = self.session.post(
                url=self.base_url + endpoint, json=json)
            response.raise_for_status()
            return response
        except Exception:
            # Forward all other exceptions/errors
            raise


class FusionRequest:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_station_list(self):
        response, body = self.session.post(endpoint='getStationList')
