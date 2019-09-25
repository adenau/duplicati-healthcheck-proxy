from falcon import testing
from hcproxy.bootstrap import Bootstrap
from pytest_httpserver import HTTPServer
import pytest
import logging

@pytest.fixture()
def test_rig():
    
    logging.basicConfig(level=logging.DEBUG)

    bootstrap = Bootstrap()

    rig = {}
    rig["client"] = testing.TestClient(bootstrap.create())
  
    yield rig

def test_success(test_rig):

    result = test_rig["client"].simulate_get('/health')

    # Did we return 200?
    assert result.status == "200 OK"