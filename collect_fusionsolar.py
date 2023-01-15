
import os
import fusionsolar

user = os.environ.get('FUSIONSOLAR_USER', 'unkown')
password = os.environ.get('FUSIONSOLAR_PASSWORD', 'unkown')

try:
    with fusionsolar.Session(user=user, password=password) as session:
            session.logout()
except Exception as e:
    print(e)
