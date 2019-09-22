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
        
        check_for_failure = ("Failed" in parsed_report.keys())

        hc_return = self.signalHealthCheck(check_id, not check_for_failure, parsed_report)

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
            response = requests.post(url, data=content)
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

        parsed_report["message"] = raw_report[0]

        if (raw_report[2][:6] == "Failed"):
            return self.parseFailedReport(raw_report, parsed_report)
        else:
            return self.parseSuccessfulReport(raw_report, parsed_report)

    def parseSuccessfulReport(self, raw_report, parsed_report):

        for line in raw_report:
            keyvalue = line.split(":",1)

            if ( len(keyvalue) > 1):
                    key = keyvalue[0]
                    value = keyvalue[1]
                    parsed_report[key] = value

        return parsed_report


    def parseFailedReport(self, raw_report, parsed_report):

        state = "Start"

        for line in raw_report:

            if (line[:7] == "Details"):
                state = "Details"
                keyvalue = line.split(":",1)
                parsed_report["Details"] = keyvalue[1]

            elif (line[:7] == "Log dat"):
                state = "LogData"
                keyvalue = line.split(":",1)
                parsed_report["Log Data"] = keyvalue[1]
            
            elif (line[:6] == "Failed"):
                state = "Failed"
                keyvalue = line.split(":",1)
                parsed_report["Failed"] = keyvalue[1]

            elif (state == "Details"):
                parsed_report["Details"] = parsed_report["Details"] + line

            elif (state == "LogData"):
                parsed_report["Log Data"] = parsed_report["Log Data"] + line

        return parsed_report
