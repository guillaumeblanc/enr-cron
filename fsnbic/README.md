# Huawei FusionSolar Northbound Interface Client

The API allows to access Huawei FusionSolar web service to download SmartPVMS data.
To login you need account on Huawei FusionSolar https://eu5.fusionsolar.huawei.com.

Implementation is based on Huawei SmartPVMS [Northbound Interface Reference V6](https://support.huawei.com/enterprise/en/doc/EDOC1100261860) documentation.

# Usage

```python
try:
    with fsnbic.ClientSession(user=user, password=password) as client:
        plants = client.get_plant_list()
        print(plants)
except fsnbic.LoginFailed:
    logging.error(
        'Login failed. Verify user and password of Northbound API account.')
    pass
```

# Running tests

Testing requires a valid Northbound API account. Tests will look for two environment variables to get user account (FUSIONSOLAR_USER) and password (FUSIONSOLAR_PASSWORD).

# Using CI

In case of a fork, these same variables (FUSIONSOLAR_USER and FUSIONSOLAR_PASSWORD) shall be added to github secrets in order for the CI to work.
