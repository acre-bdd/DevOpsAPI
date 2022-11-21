from DevOpsAPI import Wit, Step


def test_create_testrun(api):
    tr = api.TestRun.create("my testrun")
    assert tr.id > 0
    assert tr.name == "my testrun"
    assert not tr.isAutomated
