import os
import sys
import logging
import functools

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fsnbic import exception

def frequency_limit(func):
    '''Handle frequency limits cases, which cannot ben considered as fails.'''
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception.FrequencyLimit:
            logging.warning(
                'Couldn\'t complete test due to exceeding frequency limits.')
    return wrap
