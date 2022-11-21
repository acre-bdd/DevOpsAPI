import json


class TestRun:
    def __init__(self, _c, id=None, json=None):
        self._c = _c
        self._id = id
        self.json = json

    @property
    def id(self):
        return self.json['id']

    @property
    def name(self):
        return self.json['name']

    @property
    def isAutomated(self):
        return self.json['isAutomated']

    def create(self, name, automated=False):
        body = {
            "name": name,
            "automated": automated
        }

        response = self._c.post("test/runs", body, is_json=False)
        print(f"response: {json.dumps(response.json(), indent=4)}")
        return TestRun(self._c, id=None, json=response.json())
