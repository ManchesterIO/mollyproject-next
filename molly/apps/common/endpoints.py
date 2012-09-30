import json

from flask import Response

class Endpoint(object):

    def _json_response(self, response_body):
        response = Response(content_type="application/json")
        response.data = json.dumps(response_body, default=unicode)
        return response
