import json
from DevOpsApi import Api

api = Api()


class Wit:
    Epic = "Epic"
    Issue = "Issue"
    Task = "Task"
    TestCase = "Test Case"


class WorkItem:
    def __init__(self, id=None, json=None):
        if id:
            self._id = id
        if json:
            self.json = json
            self._id = self.id

    @property
    def id(self):
        return self.json['id']

    @property
    def AssignedTo(self):
        return self.fields['System.AssignedTo']['displayName']

    @property
    def Title(self):
        return self.fields["System.Title"]

    @Title.setter
    def Title(self, value):
        patches = Patches()
        patches.append(Patch(Ops.replace, "System.Title", value))
        response = api.patch(f"wit/workitems/{self.id}", patches.json(), is_json=True)
        response.raise_for_status()
        self.update()

    def update(self):
        response = api.get(f"wit/workitems/{self._id}")
        self.json = response.json()
        return self

    @property
    def fields(self):
        return self.json['fields']

    @staticmethod
    def get(id):
        return WorkItem(id).update()

    def delete(self):
        response = api.delete(f"wit/workitems/{self.id}")
        response.raise_for_status()

    @staticmethod
    def create(type, title, area=None):
        patches = Patches()
        patches.append(Patch(Ops.add, "System.Title", title))
        if area:
            patches.append(Patch(Ops.add, "System.AreaPath", area))
        response = api.post(f"wit/workitems/${type}", patches.json(), is_json=True)
        response.raise_for_status()
        return WorkItem(None, response.json())

    def __str__(self):
        return f"{self.id}: {self.title} @{self.AssignedTo}"


class WorkItems:
    def __init__(self, json=None):
        pass

    def find(filter={}):
        tokens = []
        for (attribute, value) in filter.items():
            tokens.append(f"[{attribute}] = '{value}'")
        tokenstr = " and ".join(tokens)
        ft = f"Where {tokenstr}" if len(tokens) > 0 else ""
        query = f"Select [System.Id] From WorkItems {ft}"
        search = {'query': query}
        response = api.post("wit/wiql", json=search)
        response.raise_for_status()
        return [wi['id'] for wi in response.json()['workItems']]


class Patch:
    def __init__(self, operation, field, value):
        self.operation = operation
        self.field = field
        self.value = value

    def json(self):
        result = {
            "from": None,
            "op": self.operation,
            "path": f"/fields/{self.field}",
            "value": self.value
        }
        return result


class Patches(list):
    def json(self):
        return [patch.json() for patch in self]


class Ops:
    add = "add"
    replace = "replace"

