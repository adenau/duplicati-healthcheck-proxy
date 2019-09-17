import falcon
import json

from hcproxy.controllers.duplicati import DuplicatiController

class Bootstrap(object):

    #_testMode = False

    def create(self, hc_override=""):

        self.app = falcon.API()
        self.app.add_route('/duplicati', DuplicatiController(hc_override=""))

        return self.app