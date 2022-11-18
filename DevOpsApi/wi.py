import json

from DevOpsApi import Api

api = Api()


class Wit:
    TestCase = "Test Case"


class WorkItem:
    def __init__(self, json=None):
        self.json = json

    @property
    def id(self):
        return self.json['id']

    @property
    def assigned(self):
        return self.fields['System.AssignedTo']['displayName']

    @property
    def title(self):
        return self.fields['System.Title']

    @property
    def fields(self):
        return self.json['fields']

    @staticmethod
    def get(id):
        response = api.get(f"wit/workitems/{id}")
        return WorkItem(response.json())

    @staticmethod
    def create(type, title):
        patch = Patch(Ops.add, "System.Title", title)
        response = api.post(f"wit/workitems/${type}", patch.json(), is_json=True)
        print("******")
        print(json.dumps(response.json(), indent=4))
        print("******")
        response.raise_for_status()
        return WorkItem(response.json())

    def __str__(self):
        return f"{self.id}: {self.title} @{self.assigned}"


class WorkItems:
    def __init__(self, json=None):
        pass

    def find(filter={}):
        tokens = []
        for (attribute, value) in filter.items():
            tokens.append(f"[{attribute}] = 'value'")
        tokenstr = " and ".join(tokens)
        ft = f"Where {tokenstr}" if len(tokens) > 0 else ""
        query = f"Select [System.Id] From WorkItems {ft}"
        search = {'query': query}
        response = api.post("wit/wiql", json=search)
        print(json.dumps(response.json(), indent=4))
        response.raise_for_status()
        print(response.text)


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
        return [result]


class Ops:
    add = "add"
