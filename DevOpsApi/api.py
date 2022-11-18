import requests


class Api:
    def __init__(self):
        self.organization = "ck0548"
        self.project = "acre"
        self.headers = {'Content-type': 'application/json-patch+json'}
        self.user = "ck@realtime-projects.com"
        self.apikey = "hctd4coz47i4qc6pd3dl5wml6dwf4jio5hqc44ykafrf3zv7khsa"

    @property
    def auth(self):
        return (self.user, self.apikey)

    def uri(self, fnc):
        return f"https://dev.azure.com/{self.organization}/{self.project}/_apis/{fnc}?api-version=7.0"

    def get(self, fnc, json=None):
        return requests.get(self.uri(fnc), auth=self.auth, headers=self.headers, json=json)

    def post(self, fnc, json=None, is_json=False):
        headers = self.headers if is_json else None
        return requests.post(self.uri(fnc), auth=self.auth, headers=headers, json=json)

    def patch(self, fnc, json=None, is_json=False):
        headers = self.headers if is_json else None
        return requests.patch(self.uri(fnc), auth=self.auth, headers=headers, json=json)

    def delete(self, fnc):
        return requests.delete(self.uri(fnc), auth=self.auth)
