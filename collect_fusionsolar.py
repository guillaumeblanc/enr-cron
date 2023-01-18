import os
import sys
import logging

if os.environ.get('FUSIONSOLAR_USER') is None:
    logging.error('Missing environment variable FUSIONSOLAR_USER')
    sys.exit(os.EX_DATAERR)
user = os.environ.get('FUSIONSOLAR_USER', 'unkown')

if os.environ.get('FUSIONSOLAR_PASSWORD') is None:
    logging.error('Missing environment variable FUSIONSOLAR_PASSWORD')
    sys.exit(os.EX_DATAERR)
password = os.environ.get('FUSIONSOLAR_PASSWORD', 'unkown')
