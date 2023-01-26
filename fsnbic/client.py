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

    # Get basic plants information.
    # Implementation wraps a call to the Plant List Interface, as documented in 7.1.3
    def get_plant_list(self):
        return self.session.post(endpoint='getStationList')['data']

    # Get real-time plant data by plant ID set.
    # Implementation wraps a call to the Plant Data Interfaces, as documented in 7.1.4
    # Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
    # Data of a maximum of 100 plants can be queried at a time.
    # For details about the data list that can be queried using this interface, see 7.2.1 Interface for Real-time Plant Data.
    def get_plant_data(self, plants):  # : list(str)
        # {"stationCodes": "BA4372D08E014822AB065017416F254C,5D02E8B40AD342159AC8D8A2BCD4FAB5"}'
        plants_json = "{'stationCodes':''}"
        try:
            return self.session.post(endpoint='getKpiStationHour', json=plants_json)
        except Exception as e:
            raise


class ClientSession(Client):
    def __init__(self, user: str, password: str):
        return super().__init__(session=session.Session(user=user, password=password))

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)
