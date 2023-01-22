import os
import sys
import logging

import fsnbic

if os.environ.get('FUSIONSOLAR_USER') is None:
    logging.error('Missing environment variable FUSIONSOLAR_USER')
    sys.exit(os.EX_DATAERR)
user = os.environ.get('FUSIONSOLAR_USER', 'unkown')

if os.environ.get('FUSIONSOLAR_PASSWORD') is None:
    logging.error('Missing environment variable FUSIONSOLAR_PASSWORD')
    sys.exit(os.EX_DATAERR)
password = os.environ.get('FUSIONSOLAR_PASSWORD', 'unkown')

try:
    with fsnbic.ClientSession(user=user, password=password) as client:
        plants = client.get_plant_list()
        print(plants)
except fsnbic.LoginFailed:
    logging.error(
        'Login failed. Verify user and password of Northbound API account.')
    pass
except fsnbic.FrequencyLimit:
    logging.error('The interface access frequency is too high.')
    pass
