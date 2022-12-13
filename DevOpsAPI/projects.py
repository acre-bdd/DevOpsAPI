from .connection import Connection
from .base import FunctionClass, FunctionManager
import json


class Project(FunctionClass):
    def __init__(self, _c, json=None):
        _c = Connection(_c.organization, None, _c.user, _c.apikey)
        super().__init__("projects", _c, json)


class Projects(FunctionManager):
    def __init__(self, _c):
        _c = Connection(_c.organization, None, _c.user, _c.apikey)
        super().__init__("projects", _class=Project, _c=_c)

    def get(self, id):
        return Project(self._c, json=self.get_properties(id))


def _dump(response):
    print(f"response: {json.dumps(response.json(), indent=4)}")
