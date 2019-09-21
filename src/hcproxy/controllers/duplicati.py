import urllib.parse
import falcon
import json
import requests
import logging
import pprint

class DuplicatiController(object):

    _hc_url = "https://hc-ping.com/"

    def __init__(self, hc_override = None):

        logging.debug("[DuplicatiController] : Initializing")

        if (hc_override != None):
            self._hc_url = hc_override
            logging.debug("[DuplicatiController] : Setting override of {}".format(hc_override) )

    def on_post(self, req, resp, check_id):

        logging.info("[DuplicatiController] : Received POST from {}".format(req) )

        parsed_report = self.parseReport(req.bounded_stream.read().decode("utf-8"))
        check_for_success = "Failed:" in parsed_report.keys()

        hc_return = self.signalHealthCheck(check_id, check_for_success, parsed_report)

        if hc_return:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500

        resp_content = { "data" : parsed_report }
        resp.body = json.dumps(resp_content)

    def signalHealthCheck(self, check_id, success, content):

        url = self._hc_url + check_id

        if(success == False):
            url = url + "/fail"

        logging.debug("[DuplicatiController] : Sending ping to HealthCheck at {}".format(url) )

        try:
            response = requests.post(url, data={'key':'value'})
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logging.error("[DuplicatiController] Unable to reach Healthcheck server {}".format(e))
            return False

        if response.status_code == 200:
            return True

        return False

    def parseReport(self, content):

        body_content = urllib.parse.unquote(content)

        raw_report = body_content.splitlines()
        parsed_report = {}

        for line in raw_report:

            previous_key = ""

            if (line[:1] == " "):
                parsed_report[previous_key] = parsed_report[previous_key] + line
            else:
                keyvalue = line.split()

                if ( len(keyvalue) > 1):
                    key = keyvalue[0]
                    value = keyvalue[1]
                    parsed_report[key] = value
                else:
                    parsed_report[previous_key] = parsed_report[previous_key] + keyvalue[0]

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(parsed_report)

        return parsed_report
        


        