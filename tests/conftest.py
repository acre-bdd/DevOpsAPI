import os
import pytest

from DevOpsApi import Api


class SetupError(Exception):
    pass


msg = """
Please set the environment variables
    - ORGANISATION,
    - PROJECT,
    - USER,
    - APIKEY and
    - AREA

to proper values in order to run the test.

CAUTION: All WorkItems in devops in the given
         area WILL BE DELETED when running the test.

         Make sure you don't destroy any data
         in your devops
"""


@pytest.fixture
def area():
    area = os.environ.get('AREA')
    if not area:
        raise SetupError(msg)


@pytest.fixture
def api():
    organization = os.environ.get('ORGANIZATION')
    project = os.environ.get('PROJECT')
    user = os.environ.get('USER')
    apikey = os.environ.get('APIKEY')

    if not organization or not project or not user or not apikey:
        raise SetupError(msg)

    return Api(organization=organization,
               project=project,
               user=user,
               apikey=apikey)
