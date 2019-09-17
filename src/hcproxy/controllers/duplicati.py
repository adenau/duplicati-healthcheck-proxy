import falcon
import json

class DuplicatiController(object):

    _hc_url = "https://hc-ping.com/"

    def __init__(self, hc_override=""):

        if (hc_override != ""):
            self._hc_url = hc_override

    def on_post(self, req, resp):
        """Handles POST requests"""
        
        data = req.bounded_stream.read()
        print(data)
        
        resp.status = falcon.HTTP_200  # This is the default status
        resp_content = { "data" : data }
        resp.body = json.dumps(resp_content)

