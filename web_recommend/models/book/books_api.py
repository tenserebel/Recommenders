#https://github.com/hoffmann/googlebooks/blob/master/googlebooks.py
import requests
import json

class Api(object):

    __BASEURL = 'https://www.googleapis.com/books/v1'
    def __init__(self ):
       pass 

    def _get(self, path, params=None):
        if params is None:
            params = {}
        resp = requests.get(self.__BASEURL+path, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content)

        return resp

    def get(self, volumeId, **kwargs):
        path = '/volumes/'+volumeId
        params = dict()
        for p in 'partner projection source'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path)
    
    def list(self, q, **kwargs):
        path = '/volumes'
        params = dict(q=q)
        for p in 'download filter langRestrict libraryRestrict maxResults orderBy partner printType projection showPreorders source startIndex'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path, params)