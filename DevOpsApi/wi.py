from lxml import etree

class Wit:
    Epic = "Epic"
    Issue = "Issue"
    Task = "Task"
    TestCase = "Test Case"


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
    def WorkItemType(self):
        return self.fields['System.WorkItemType']

    @property
    def Title(self):
        return self.fields["System.Title"]

    @Title.setter
    def Title(self, value):
        patches = Patches()
        patches.append(Patch(Ops.replace, "System.Title", value))
        response = self._c.patch(f"wit/workitems/{self.id}", patches.json(), is_json=True)
        response.raise_for_status()
        self.update()

    def update(self):
        response = self._c.get(f"wit/workitems/{self._id}")
        self.json = response.json()
        return self

    @property
    def fields(self):
        return self.json['fields']

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
        response = self._c.post(f"wit/workitems/${type}", patches.json(), is_json=True)
        response.raise_for_status()
        return WorkItem(self._c, None, response.json())

    def __str__(self):
        return f"{self.id}: {self.title} @{self.AssignedTo}"


class TestCase(WorkItem):
    def create(self, title, area=None):
        wi = super().create(type=Wit.TestCase, title=title, area=area)
        return TestCase(wi._c, wi.id, wi.json)

    @property
    def steps(self):
        steps = self.fields["Microsoft.VSTS.TCM.Steps"]
        xsteps = etree.fromstring(steps)
        return [Step(st[0].text, st[1].text) for st in xsteps]

    @steps.setter
    def steps(self, steps):
        strsteps = [step.as_xml() for step in steps]
        stepxml = f'<steps>{"".join(strsteps)}</steps>'
        print(stepxml)

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
            tokens.append(f"[{attribute}] = '{value}'")
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

