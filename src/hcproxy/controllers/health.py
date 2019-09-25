import urllib.parse
import falcon
import json
import requests
import logging
import pprint

class HealthController(object):



    def __init__(self):

        logging.debug("[HealthController] : Initializing")

    def on_get(self, req, resp):

        resp.status = falcon.HTTP_200