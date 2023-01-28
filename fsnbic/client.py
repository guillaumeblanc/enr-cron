import logging
import os
import itertools

from . import session
from . import exception


class Client:
    def __init__(self, session: session.Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_plant_list(self) -> list :
        '''
        Get basic plants information.
        Implementation wraps a call to the Plant List Interface, see https://support.huawei.com/enterprise/en/doc/EDOC1100261860/4217ab29/plant-list-interface
        This implementation will query all available pages
        '''
        plants = []
        for page in itertools.count(start=1):
            param = {'pageNo': page, 'pageSize': 100}
            data = self.session.post(endpoint='getStationList', json=param)['data']
            plants = plants + data['list']
            if page >= data['pageCount']:
                return plants

    def get_plant_data(self, plants) -> dict :
        '''
        Get real-time plant data by plant ID set.
        Implementation wraps a call to the Plant Data Interfaces, see https://support.huawei.com/enterprise/en/doc/EDOC1100261860/cf4fb068/plant-data-interfaces
        Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
        Data of a maximum of 100 plants can be queried at a time.
        For details about the data list that can be queried using this interface, see https://support.huawei.com/enterprise/en/doc/EDOC1100261860/c83ecf37/interface-for-real-time-plant-data.
        '''
        if not plants:
            return {}

        plants_json = {'stationCodes':''}
        try:
            return self.session.post(endpoint='getStationRealKpi', json=plants_json)
        except exception.Exception as e:
            raise


class ClientSession(Client):
    def __init__(self, user: str, password: str):
        return super().__init__(session=session.Session(user=user, password=password))

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)
