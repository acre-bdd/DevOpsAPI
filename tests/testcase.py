from DevOpsAPI import Wit, Step


def test_create_get_delete(api, area):
    tc1 = api.TestCase.create("this is a Test Case", area=area)
    assert tc1.id > 0
    assert tc1.Title == "this is a Test Case"
    assert tc1.WorkItemType == Wit.TestCase
    tc11 = api.TestCase.get(tc1.id)
    assert tc11.id == tc1.id
    assert tc11.Title == "this is a Test Case"
    wi = api.WorkItem.get(tc1.id)
    assert wi.WorkItemType == Wit.TestCase
    tc1.delete()


def test_steps(api, area):
    tc = api.TestCase.create("Test Case with steps", area=area)
    tc.steps = [Step("in1", "out1"), Step("in2", "out2")]
    steps = tc.steps
    assert steps[0].action == "in1"
    assert steps[0].result == "out1"
    assert steps[1].action == "in2"
    assert steps[1].result == "out2"


def test_modify(api, area):
    tc = api.TestCase.create("Another Test Case", area=area)
    assert tc.Title == "Another Test Case"
    assert tc.WorkItemType == Wit.TestCase
    tc.Title = "Changed Title of Test Case"
    assert tc.Title == "Changed Title of Test Case"
    tc.delete()


def test_find(api, area):
    ids = api.WorkItems.find({"System.WorkItemType": Wit.TestCase})
    for id in ids:
        api.TestCase.get(id=id).delete()
    wi1 = api.TestCase.create("TC 1", area=area)
    wi1.Description = "This is a test case"
    wi2 = api.TestCase.create("TC 2", area=area)
    wi3 = api.TestCase.create("TC 3", area=area)
    ids = api.WorkItems.find({"System.WorkItemType": Wit.TestCase})
    assert len(ids) == 3
    assert wi1.id in ids
    assert wi2.id in ids
    wi11 = api.TestCase.get(wi1.id)
    assert wi11.Description == "This is a test case"

    assert wi3.id in ids
