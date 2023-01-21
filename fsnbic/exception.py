import logging

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
    logging.debug('failCode ' + str(failCode) + ' received with body: ' + str(body))
    return switcher.get(failCode, _FusionInternalException)(body)
