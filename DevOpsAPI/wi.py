import json
import re
from lxml import etree


class Wit:
    Epic = "Epic"
    Issue = "Issue"
    Task = "Task"
    TestCase = "Test Case"
    Requirement = "Requirement"
    Epic = "Epic"
    Feature = "Feature"


class Step:
    def __init__(self, action, result=""):
        self.action = action
        self.result = result

    def as_xml(self):
        return Step._template.format(self.action, self.result)

    def __str__(self):
        return f"Step: action: {self.action}, result: {self.result}"

    _template = """
        <step id=\"2\" type=\"ValidateStep\">
            <parameterizedString isformatted=\"true\">{}</parameterizedString>
            <parameterizedString isformatted=\"true\">{}</parameterizedString><description/>
        </step>"""


class WorkItem:
    def __init__(self, connection, id=None, json=None):
        self._c = connection

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
    def AreaPath(self):
        return self.fields['System.AreaPath']

    @AreaPath.setter
    def AreaPath(self, value):
        self._update_field("System.AreaPath", value)

    @property
    def WorkItemType(self):
        return self.fields['System.WorkItemType']

    @property
    def Description(self):
        return self.fields["System.Description"]

    @Description.setter
    def Description(self, value):
        self._update_field("System.Description", value)

    @property
    def Title(self):
        return self.fields["System.Title"]

    @Title.setter
    def Title(self, value):
        self._update_field("System.Title", value)

    @property
    def Tags(self):
        return self.fields["System.Tags"]

    @Tags.setter
    def Tags(self, value):
        self._update_field("System.Tags", value)

    def _update_field(self, fieldname, value):
        patches = Patches()
        patches.append(Patch(Ops.replace, fieldname, value))
        response = self._c.patch(f"wit/workitems/{self.id}", json=patches.json(), is_json=True)
        if response.status_code != 200:
            print(json.dumps(response.json(), indent=4))
        response.raise_for_status()
        self.update()

    def update(self):
        # self._c.get("wit/fields")
        response = self._c.get(f"wit/workitems/{self._id}", expand="relations")
        self.json = response.json()
        return self

    @property
    def fields(self):
        return self.json['fields']

    @property
    def childs(self):
        ids = []
        for relation in self.json['relations']:
            if relation['rel'] != "System.LinkTypes.Hierarchy-Forward":
                continue
            m = re.match(r'https.*/(\d+)$', relation['url'])
            ids.append(int(m.group(1)))
        return ids

    def get(self, id):
        return WorkItem(self._c, id).update()

    def delete(self):
        response = self._c.delete(f"wit/workitems/{self.id}")
        response.raise_for_status()

    def create(self, type, title, area=None):
        patches = Patches()
        patches.append(Patch(Ops.add, "System.Title", title))
        if area:
            patches.append(Patch(Ops.add, "System.AreaPath", area))
        response = self._c.post(fnc=f"wit/workitems/${type}", json=patches.json(), is_json=True)
        response.raise_for_status()
        return WorkItem(self._c, None, response.json())

    def __str__(self):
        return f"{self.id}: {self.title} @{self.AssignedTo}"

    def __getattr__(self, name):
        _lookups = [f"System.{name}", f"Custom.{name}", name]
        for lookup in _lookups:
            if lookup in self.fields:
                return self.fields[lookup]
        return None


class TestCase(WorkItem):
    def create(self, title, area=None):
        wi = super().create(type=Wit.TestCase, title=title, area=area)
        return TestCase(wi._c, wi.id, wi.json)

    @property
    def Steps(self):
        steps = self.fields["Microsoft.VSTS.TCM.Steps"]
        xsteps = etree.fromstring(steps)
        return [Step(st[0].text, st[1].text) for st in xsteps]

    @Steps.setter
    def Steps(self, steps):
        strsteps = [step.as_xml() for step in steps]
        stepxml = f'<steps>{"".join(strsteps)}</steps>'

        patches = Patches()
        patches.append(Patch(Ops.add, "Microsoft.VSTS.TCM.Steps", stepxml))
        response = self._c.patch(f"wit/workitems/{self.id}", patches.json(), is_json=True)
        response.raise_for_status()
        self.update()

    def delete(self):
        response = self._c.delete(f"test/testcases/{self.id}")
        response.raise_for_status()

    def get(self, id):
        wi = WorkItem(self._c, id).update()
        return TestCase(wi._c, wi.id, wi.json)


class WorkItems:
    def __init__(self, connection):
        self._c = connection

    def find(self, filter={}):
        tokens = []
        for (attribute, value) in filter.items():
            if isinstance(value, dict):
                (op, value) = list(value.items())[0]
            elif value[0] == "~":
                value = value[1:]
                op = "Contains"
            else:
                op = "="
            tokens.append(f"[{attribute}] {op} '{value}'")
        tokenstr = " and ".join(tokens)
        ft = f"Where {tokenstr}" if len(tokens) > 0 else ""
        query = f"Select [System.Id] From WorkItems {ft}"
        search = {'query': query}
        response = self._c.post("wit/wiql", json=search)
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
