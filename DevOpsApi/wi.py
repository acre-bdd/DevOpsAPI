import json
import requests


organization = "ck0548"
project = "acre"
headers = {'Content-type': 'application/json-patch+json'}
user = "ck@realtime-projects.com"
apikey = "hctd4coz47i4qc6pd3dl5wml6dwf4jio5hqc44ykafrf3zv7khsa"
auth = (user, apikey)


class Ops:
    add = "add"


class Wit:
    testcase = "Test Case"


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
        uri = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0"
        response = requests.get(uri, auth=auth, headers=headers)
        return WorkItem(response.json())

    @staticmethod
    def create(type, title):
        uri = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${type}?api-version=7.0"
        patch = Patch(Ops.add, "System.Title", title)
        response = requests.post(uri, auth=auth, headers=headers, json=patch.json())
        return WorkItem(response.json())
        print(json.dumps(response.json(), indent=4))

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
        uri = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.0"
        response = requests.post(uri, json=search, auth=auth)
        print(json.dumps(response.json(), indent=4))
        response.raise_for_status()
        print(response.text)


