import falcon
import json

from hcproxy.controllers.duplicati import DuplicatiController

class Bootstrap(object):

    #_testMode = False

    def create(self, hc_override = None):

        self.app = falcon.API()
        self.app.add_route('/duplicati/{check_id}', DuplicatiController(hc_override=hc_override))

        return self.app