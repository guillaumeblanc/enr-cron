import logging
import os
import requests
import json
import functools

from . import exception

# Based on documentation iMaster NetEco V600R023C00 Northbound Interface Reference-V6(SmartPVMS)
# https://support.huawei.com/enterprise/en/doc/EDOC1100261860


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
            except exception._305_NotLogged:
                login_again = True

    return wrap


def validate(func):
    '''Ensures requests succeeds'''

    @functools.wraps(func)
    def wrap(*args, **kwargs) -> tuple[requests.Response, dict]:
        response = func(*args, **kwargs)
        body = response.json()
        if not body.get('success', False):
            raise exception._FailCodeToException(body)
        return response, body
    return wrap


def exceptions_sanity(func):
    '''Ensures sanity of exceptions raised to the public API. No internal exception should get to public side.'''

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception._InternalException as e:
            logging.exception(
                'Internal exceptions getting out of of the private code.')
            raise exception.Exception()

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
        '''
        Login to base url
        See documentation: https://support.huawei.com/enterprise/en/doc/EDOC1100261860/9e1a18d2/login-interface
        '''

        try:
            # Posts login request
            self.session.cookies.clear()
            response, body = self._raw_post(endpoint='login', parameters={
                'userName': self.user, 'systemCode': self.password})
            # Login succeeded, stores authentication token
            self.session.headers.update(
                {'XSRF-TOKEN': response.cookies.get(name='XSRF-TOKEN')})
        except exception._305_NotLogged:
            # Login failed can also be raised directly for 20001, 20002, 20003 failCodes.
            raise exception.LoginFailed() from None
        except json.JSONDecodeError:
            # FusionSolar NBI sends an empty json when user is unknown. It's not the expected behavior described by documentation 7.1.1.
            # It's caught here with JSONDecodeError exception.
            raise exception.LoginFailed() from None

    @exceptions_sanity  # Must be the first decorator.
    @logged
    def post(self, endpoint, parameters={}) :
        '''Executes POST request'''
        response, body = self._raw_post(endpoint, parameters)
        return body

    @validate
    def _raw_post(self, endpoint, parameters={}) -> requests.Response:
        '''Executes POST request'''
        response = self.session.post(url=self.base_url + endpoint, json=parameters)
        response.raise_for_status()
        return response

