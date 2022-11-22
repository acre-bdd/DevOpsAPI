import json as js
import requests
import logging


class Connection:
    def __init__(self, organization, project, user, apikey):
        self.organization = organization
        self.project = project
        self.user = user
        self.apikey = apikey
        self.headers = {'Content-type': 'application/json-patch+json'}

    def get(self, *args, **kwargs):
        return self.request("get", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("delete", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("post", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request("patch", *args, **kwargs)

    def request(self, rt, fnc, json=None, is_json=False):
        headers = self.headers if is_json else None
        print(f"calling: {rt}:{self._uri(fnc)}")
        response = requests.request(rt, self._uri(fnc), json=json, auth=self._auth, headers=headers)
        if response.status_code >= 300:
            print(js.dumps(response.json(), indent=4))
            logging.warning(js.dumps(response.json(), indent=4))
            response.raise_for_status()
        return response

    @property
    def _auth(self):
        return (self.user, self.apikey)

    def _uri(self, fnc):
        project = f"/{self.project}" if self.project else ""
        return f"https://dev.azure.com/{self.organization}{project}/_apis/{fnc}?api-version=7.0"

    
