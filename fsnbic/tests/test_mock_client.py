import os
import sys
import logging
import unittest
import datetime
import csv

import pandas as pd

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

from fsnbic.tests.mock_session import *
import fsnbic

def to_table(data):
    for entry in data:
        line = entry['dataItemMap']
        line['stationCode'] = entry['stationCode']
        line['currentTime'] = entry.get('currentTime', 0)
        yield line

class TestPandasClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = fsnbic.Client(MockSession())

    def test(self):
        now = datetime.datetime.now()

       # t = now.strftime("%Y-%m-%d_%H-%M")
       # print("Time:", t)

        # All plants
        plants_raw = self.client.get_plant_list()
        pd.DataFrame(plants_raw).to_csv('plants.csv', index=False)

        # List of plant codes
        plants_code = [plant['stationCode'] for plant in plants_raw]

        # Realtime KPIs (with fake station)
        realtime = self.client.get_plant_realtime_data(plants_code + ['UnknownStationCode'])
        self.assertGreaterEqual(len(plants_code), len(realtime))

        # Hourly data
        hourly = self.client.get_plant_hourly_data(plants_code, now)
        #ht = to_table(hourly)

        #p = pd.DataFrame(ht)
        #p.to_csv('hourly.csv', index=False)

        # Daily data
        daily = self.client.get_plant_daily_data(plants_code, now)

        # Monthly data
        monthly = self.client.get_plant_monthly_data(plants_code, now)

        # Yearly data
        yearly = self.client.get_plant_yearly_data(plants_code, now)
        

if __name__ == '__main__':
    unittest.main()
