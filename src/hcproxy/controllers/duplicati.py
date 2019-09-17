import falcon
import json

class DuplicatiController(object):

    def on_post(self, req, resp):
        """Handles POST requests"""
        
        data = req.bounded_stream.read()
        print(data)
        
        resp.status = falcon.HTTP_200  # This is the default status
        resp_content = {}
        resp.body = json.dumps(resp_content)