
import requests
import os
import pandas as pd

from extern.FusionSolar import fusionsolar

user = os.environ.get('FUSIONSOLAR_USER', 'unkown')
password = os.environ.get('FUSIONSOLAR_PASSWORD', 'unkown')

date = pd.Timestamp('20200402', tz='Europe/Brussels')

try:
    with fusionsolar.PandasClient(user_name=user, system_code=password) as client:
        sl = client.get_station_list()
        station_code = sl['data'][0]['stationCode']

        df = client.get_kpi_day(station_code=station_code, date=date)
        print(df)
except Exception as e:
    print(e)
