from falcon import testing
from dhp.bootstrap import Bootstrap
import pytest


# Depending on your testing strategy and how your application
# manages state, you may be able to broaden the fixture scope
# beyond the default 'function' scope used in this example.

@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    bootstrap = Bootstrap()
    return testing.TestClient(bootstrap.create())


def test_get_message(client):
    doc = {u'message': u'Hello world!'}

    result = client.simulate_get('/things')
    assert result.json == doc