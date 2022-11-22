import pytest
import json

from DevOpsAPI import Wit, Step, TestResult


@pytest.fixture
def testplan(api):
    tp = api.TestPlans.create(name="pytest_testplan")
    yield tp
    tp.delete()


def test_list_testruns(api):
    truns = api.TestRuns.list()
    print([tr.name for tr in truns])


def test_get_testresults(api):
    tr = api.TestResults.get(32)


def test_get_testrun(api):
    tr = api.TestRun.get(32)
    

def xtest_create_keep(api):
    tp = api.TestPlans.create(name="my testplan")


def test_create_list_delete_testplan(api):
    tp = api.TestPlans.create(name="automated testplan")
    assert tp.name == "automated testplan"
    assert tp.id > 0
    tpl = api.TestPlans.list()
    assert tp.name in [tp.name for tp in tpl]
    tp.delete()
    tpl = api.TestPlans.list()
    assert tp.name not in [tp.name for tp in tpl]


def test_create_list_delete_testruns(api):
    tr1 = api.TestRuns.create(name="tmp_testrun")
    tr2 = api.TestRuns.create(name="tmp_testrun")
    tr3 = api.TestRuns.create(name="tmp_testrun")
    trs = api.TestRuns.list()
    for tr in (tr1, tr2, tr3):
        assert tr.name in [ltr.name for ltr in trs]
    trs = api.TestRuns.list()
    for tr in trs:
        if tr.name == "tmp_testrun" and tr.state != "255":
            print(json.dumps(tr.json, indent=4))
            tr.delete()
    trs = api.TestRuns.list()
    print([tr.name for tr in trs])
    for tr in trs:
        assert "tmp_testrun" not in tr.name or tr.state == "255"


def test_add_testrun_to_testplan(testplan, area, api):
    tp = api.TestPlans.create(name="pytest_addtestrun")
    ts = tp.suites[0]
    assert ts.name == "pytest_addtestrun"
    assert len(ts.TestCases.list()) == 0
    tc = ts.TestCases.add([310])
    print(tc)
    tcs = ts.TestCases.list()
    assert len(tcs) == 1
    assert tcs[0].id == str(310)
    # tc1 = api.TestCase.create("pytest_addtestrun_testcase1", area=area)
    # tp.add_testcase(tc1)
    # tr = api.TestRuns.create(name="testrun1", plan={'id': tp.id})
    # assert tr


def test_create_testrun(api):
    tr = api.TestRuns.create(name="create_testrun")
    assert tr.id > 0
    assert tr.name == "create_testrun"
    assert not tr.isAutomated
    tr.delete()


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

