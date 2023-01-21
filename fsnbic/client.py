import logging
import os
from . import session

class Client:
    def __init__(self, session: session.Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_station_list(self):
        response, body = self.session.post(endpoint='getStationList')

