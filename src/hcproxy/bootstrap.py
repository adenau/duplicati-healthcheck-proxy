import falcon
import json

from hcproxy.controllers.duplicati import DuplicatiController

class Bootstrap(object):

    #_testMode = False

    def create(self):

        self.app = falcon.API()
        self.app.add_route('/duplicati', DuplicatiController())

        return self.app