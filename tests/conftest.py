import pytest

from DevOpsApi import Api


@pytest.fixture
def api():
    return Api(organization="ck0548",
               project="acre",
               user="ck@realtime-projects.com",
               apikey="hctd4coz47i4qc6pd3dl5wml6dwf4jio5hqc44ykafrf3zv7khsa")
