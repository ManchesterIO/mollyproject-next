import json

from flask import Response, abort, request

class Endpoint(object):

    def _json_response(self, response_body):
        if not request.accept_mimetypes.accept_json:
            abort(406)
        response = Response(content_type="application/json")
        response.data = json.dumps(response_body, default=unicode)
        return response
