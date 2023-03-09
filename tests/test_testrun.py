import pytest
import json

from DevOpsAPI import TestResult


@pytest.fixture
def testplan(api):
    tp = api.TestPlans.create(name="pytest_testplan")
    yield tp
    tp.delete()


@pytest.fixture
def testrun(api):
    tr = api.TestRuns.create(name="pytest_testrun")
    yield tr
    tr.delete()


@pytest.fixture
def testcase(api, area):
    tc = api.TestCase.create("this is a Test Case", area=area)
    yield tc
    tc.delete()


def test_get_testrun(testrun, api):
    tr2 = api.TestRuns.get(testrun.id)
    assert tr2.id == testrun.id
    assert tr2.name == testrun.name


def disabled_test_delete_all_testplans(api):
    tpl = api.TestPlans.list()
    for tp in tpl:
        tp.delete()


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
            tr.delete()
    trs = api.TestRuns.list()
    for tr in trs:
        assert "tmp_testrun" not in tr.name or tr.state == "255"


def test_add_testrun_to_testplan(testplan, testcase, area, api):
    tp = api.TestPlans.create(name="pytest_addtestrun")
    ts = tp.suites[0]
    assert ts.name == "pytest_addtestrun"
    assert len(ts.TestCases.list()) == 0
    ts.TestCases.add([testcase.id])
    tcs = ts.TestCases.list()
    assert len(tcs) == 1
    assert tcs[0].id == testcase.id
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


def disabled_test_add_testresults(testcase, api, area):
    wi2 = api.TestCase.create("Another testcase", area=area)
    _dump2(wi2.json)
    tr = api.TestRuns.create(name="add_testcases", automated=False)
    assert tr.id > 0
    assert tr.name == "add_testcases"
    assert not tr.isAutomated
    r1 = TestResult(TestResult.Outcome.passed, str(testcase.id))
    assert tr.add(r1)


def _dump2(js):
    print(f"response: {json.dumps(js, indent=4)}")
