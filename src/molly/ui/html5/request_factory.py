from httplib import HTTPConnection, HTTPException
import socket

class HttpRequestFactory(object):

    RequestException = HTTPException

    def __init__(self, hostname, port=80):
        self._hostname = hostname
        self._port = port

    def request(self, path):
        connection = HTTPConnection(self._hostname, self._port)
        try:
            connection.request('GET', path, headers={
                'Accept': 'application/json'
            })
        except socket.error:
            raise self.RequestException(socket.error)
        return connection.getresponse()
