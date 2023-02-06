import logging
import os
import itertools
import datetime

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
        Implementation wraps a call to the Plant List Interface, see documentation 7.1.3
        This implementation will query all available pages
        '''
        plants = []
        for page in itertools.count(start=1):
            param = {'pageNo': page, 'pageSize': 100}
            data = self.session.post(endpoint='getStationList', parameters=param)['data']
            plants = plants + (data['list'] if data['list'] else [])
            if page >= data['pageCount']:
                return plants

    # Batches calls to by groups of 'batch_size' plants. 100 is the usual limit for FusionSolar
    def _get_plant_data(self, endpoint, plants: list, parameters = {}, batch_size = 100) -> list :
        data = []
        for batch in [plants[i:i + batch_size] for i in range(0, len(plants), batch_size)]:
            parameters['stationCodes'] = ','.join(plants)
            response = self.session.post(endpoint=endpoint, parameters=parameters)
            data = data + (response['data'] if response['data'] else [])
        return data

    def get_plant_realtime_data(self, plants: list) -> list :
        '''
        Get real-time plant data by plant ID set.
        Implementation wraps a call to the Plant Data Interfaces, see 7.1.4.1
        Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
        '''
        return self._get_plant_data('getStationRealKpi', plants)

    def _get_plant_timed_data(self, endpoint, plants: list, date = datetime.datetime) -> list:
        '''
        Internal function for getting plant data by plants ID set and date.
        '''
        # Time is in milliseconds
        parameters = {'collectTime': int(date.timestamp() * 1e3)}
        return self._get_plant_data(endpoint, plants, parameters)

    def get_plant_hourly_data(self, plants: list, date = datetime.time) -> list:
        '''
        Get hourly plant data by plants ID set.
        Implementation wraps a call to the Plant Hourly Data Interfaces, see 7.1.4.2
        Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
        '''
        return self._get_plant_timed_data('getKpiStationHour', plants=plants, date=date)

    def get_plant_daily_data(self, plants: list, date = datetime.time) -> list:
        '''
        Get daily plant data by plants ID set.
        Implementation wraps a call to the Plant Hourly Data Interfaces, see 7.1.4.3
        Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
        '''
        return self._get_plant_timed_data('getKpiStationDay', plants=plants, date=date)
        
    def get_plant_monthly_data(self, plants: list, date = datetime.time) -> list:
        '''
        Get monthly plant data by plants ID set.
        Implementation wraps a call to the Plant Hourly Data Interfaces, see 7.1.4.4
        Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
        '''
        return self._get_plant_timed_data('getKpiStationMonth', plants=plants, date=date)

    def get_plant_yearly_data(self, plants: list, date = datetime.time) -> list:
        '''
        Get yearly plant data by plants ID set.
        Implementation wraps a call to the Plant Hourly Data Interfaces, see 7.1.4.5
        Plant IDs can be obtained by querying get_plant_list, they are stationCode parameters.
        '''
        return self._get_plant_timed_data('getKpiStationYear', plants=plants, date=date)

class ClientSession(Client):
    def __init__(self, user: str, password: str):
        return super().__init__(session=session.Session(user=user, password=password))

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)
