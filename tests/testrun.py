import json
from DevOpsAPI import Wit, Step, TestResult


def test_list_testruns(api):
    truns = api.TestRuns.list()
    print([tr.name for tr in truns])


def test_get_testresults(api):
    tr = api.TestResults.get(32)


def test_get_testrun(api):
    tr = api.TestRun.get(32)
    

def test_create_list_delete_testplan(api):
    tp = api.TestPlans.create(name="automated testplan")
    assert tp.name == "automated testplan"
    assert tp.id > 0
    tpl = api.TestPlans.list()
    assert tp.name in [tp.name for tp in tpl]
    tp.delete()
    tpl = api.TestPlans.list()
    assert tp.name not in [tp.name for tp in tpl]


def test_create_testrun(api):
    tr = api.TestRuns.create(name="create_testrun")
    assert tr.id > 0
    assert tr.name == "create_testrun"
    assert not tr.isAutomated


def test_add_testresults(api, area):
    pl = api.Projects.list()

    wi2 = api.TestCase.create("Another testcase", area=area)
    _dump2(wi2.json)
    tr = api.TestRun.create("add_testcases", automated=False)
    assert tr.id > 0
    assert tr.name == "add_testcases"
    assert not tr.isAutomated
    r1 = TestResult(TestResult.Outcome.passed, "310")
    assert tr.add(r1)

def _dump2(js):
    print(f"response: {json.dumps(js, indent=4)}")

