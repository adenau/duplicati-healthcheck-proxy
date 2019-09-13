# Let's get this party started!
import falcon
import json

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp_content = {}
        resp_content['message'] = 'Hello world!'
        resp.body = json.dumps(resp_content)

class Bootstrap(object):

    def create(self):

        self.app = falcon.API()
        self.things = ThingsResource()
        self.app.add_route('/things', self.things)

        return self.app