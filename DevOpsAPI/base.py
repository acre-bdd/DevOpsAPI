from .connection import Connection
import json


class FunctionClass:
    def __init__(self, fnc, _c, json=None):
        self.fnc = fnc
        self._c = _c
        self.json = json

    def delete(self):
        self._c.delete(f"{self.fnc}/{self.id}")

    def __getattr__(self, name):
        return self.json[name]


class FunctionManager:
    def __init__(self, fnc, _class, _c, is_json=False):
        self._class = _class
        self._c = _c
        self.fnc = fnc
        self.is_json = is_json

    def list(self):
        return self._list(self._class)

    def get(self, id):
        return self._class(self._c, json=self.get_properties(id))

    def create(self, **kwargs):
        return self._class(self._c, self._create(kwargs))

    def _list(self, classdef=None):
        response = self._c.get(self.fnc)
        if classdef:
            return [classdef(self._c, json=js) for js in response.json()['value']]
        else:
            return response.json()['values']

    def get_properties(self, id):
        response = self._c.get(f"/{self.fnc}/{id}")
        _dump(response)
        return response.json()

    def _create(self, data):
        response = self._c.post(self.fnc, json=data, is_json=self.is_json)
        print(f"response: {_dump(response)}")
        return response.json()


def _dump(response):
    print(f"response: {json.dumps(response.json(), indent=4)}")
