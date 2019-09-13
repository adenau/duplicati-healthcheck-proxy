import falcon
import json

class DuplicatiController(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        
        print(req)
        
        resp.status = falcon.HTTP_200  # This is the default status
        resp_content = {}
        resp.body = json.dumps(resp_content)