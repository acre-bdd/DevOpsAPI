from enum import Enum
import json
import logging

from .base import FunctionManager, FunctionClass

log = logging.getLogger(__name__)


class TestResult:
    class State(Enum):
        Unspecified = 0
        NotStarted = 1
        InProgress = 2
        Completed = 3
        Aborted = 4
        Waiting = 5

    class Outcome:
        unspecified = "Unspecified"
        none = "None"
        passed = "Passed"
        failed = "Failed"
        inconclusive = "Inconclusive"
        timeout = "Timeout"
        aborted = "Aborted"
        blocked = "Blocked"
        notexecuted = "NotExecuted"
        warning = "warning"
        error = "error"
        notapplicable = "NotAppplicable"
        paused = "Paused"
        inprogress = "InProgress"
        notimpacted = "NotImpacted"

    def __init__(self, outcome, tcid, testpointid, testconfigurationid, title, rev):
        self._data = {
            "TestCase": {"id": tcid},
            "testPoint": {"id": testpointid},
            "testCaseTitle": title,
            "testCaseRevision": rev,
            "testCaseReferenceId": tcid,
            "configuration": {"id": testconfigurationid},
            "outcome": outcome,
            "customFields": {}
        }

    def set(self, name, value):
        self._data[name] = value

    def setCustomField(self, name, value):
        self._data['customFields'][name] = value


class TestResults:
    def __init__(self, connection):
        self._c = connection

    def get(self, runid):
        response = self._c.get(f"test/Runs/{runid}/results?detailstoInclude=WorkItems")
        _dump(response)


class TestPoint(FunctionClass):
    def __init__(self, _c, json=None):
        return super().__init__("test/Plans", _c, json)

    @property
    def TestConfiguration(self):
        return TestConfigurations(self._c).get(self.configuration['id'])


class TestPoints(FunctionManager):
    def __init__(self, _c, planid, suiteid):
        super().__init__(f"test/Plans/{planid}/Suites/{suiteid}/points", TestPoint, _c, is_json=False)

    def find(self, tcid):
        query = f"?testCaseId={tcid}&isRecursive=true"
        response = self._c.get(self.fnc + query)
        return [TestPoint(self._c, json=js) for js in response.json()['value']]


class TestRun(FunctionClass):
    def __init__(self, _c, json=None):
        return super().__init__("test/runs", _c, json)

    def add(self, result):
        body = [result._data]
        logging.debug(body)
        response = self._c.post(f"test/runs/{self.id}/results", json=body, is_json=False)
        _dump(response)

    def close(self, state="Completed"):
        self.set('state', state)


class TestRuns(FunctionManager):
    def __init__(self, _c):
        super().__init__("test/runs", TestRun, _c, is_json=False)


class TestConfiguration(FunctionClass):
    def __init__(self, _c, json=None):
        return super().__init__("testplan/configurations", _c, json)

    @property
    def values(self):
        _result = {}
        for value in self.json['values']:
            _result[value['name']] = value['value']
        return _result


class TestConfigurations(FunctionManager):
    def __init__(self, _c):
        super().__init__("testplan/configurations", TestConfiguration, _c, is_json=False)


class TestSuiteTestCase(FunctionClass):
    def __init__(self, _c, json=None):
        super().__init__("test/Plans/{self.planid}/suites/{self.suiteid}/testcases", _c, json)
        # _dump2(json)

    @property
    def id(self):
        return int(self.testCase['id'])

    @property
    def configurations(self):
        _result = []
        pas = self.pointAssignments
        for pa in pas:
            pac = pa['configuration']
            _result.append(TestConfigurations(self._c).get(pac['id']))
        return _result


class TestSuiteTestCases(FunctionManager):
    def __init__(self, _c, planid, suiteid):
        self.planid = planid
        self.suiteid = suiteid
        super().__init__(f"test/Plans/{self.planid}/suites/{self.suiteid}/testcases", TestSuiteTestCase, _c, json)

    def add(self, ids):
        ids = [str(id) for id in ids]
        self._c.post(f"{self.fnc}/{','.join(ids)}")


class TestSuite(FunctionClass):
    def __init__(self, _c, json=None):
        self.planid = None
        super().__init__("test/Plans/{self.planid}/suites", _c, json)

    @property
    def TestCases(self):
        return TestSuiteTestCases(self._c, self.planid, self.id)

    @property
    def TestPoints(self):
        return TestPoints(self._c, planid=self.planid, suiteid=self.id)


# class TestPlanSuiteTestCases(FunctionManager):


class TestPlanSuites(FunctionManager):
    def __init__(self, _c, planid):
        self.planid = planid
        super().__init__(f"testplan/Plans/{planid}/suites", TestSuite, _c, is_json=False)

    def list(self):
        suites = super().list()
        for suite in suites:
            suite.planid = self.planid
        return suites


class TestPlan(FunctionClass):
    def __init__(self, _c, json):
        return super().__init__("testplan/plans", _c, json)

    @property
    def suites(self):
        return TestPlanSuites(self._c, planid=self.id).list()


class TestPlans(FunctionManager):
    def __init__(self, _c):
        super().__init__("testplan/plans", TestPlan, _c)


def _dump2(js):
    logging.debug(json.dumps(js, indent=4))


def _dump(response):
    log.debug(f"response: {json.dumps(response.json(), indent=4)}")
