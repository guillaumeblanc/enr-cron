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

    def get_plant_list(self):
        return self.session.post(endpoint='getStationList')


class ClientSession(Client):
    def __init__(self, user: str, password: str):
        return super().__init__(session=session.Session(user=user, password=password))

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)
