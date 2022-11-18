from DevOpsApi.wi import WorkItem, WorkItems, Wit


def test_create_get_workitem():
    wi2 = WorkItem.create(Wit.testcase, "blablub")
    assert wi2.id > 0
    assert wi2.title == "blablub"
    wi = WorkItem.get(wi2.id)
    assert wi.id == wi2.id
    assert wi.title == "blablub"


def test_list_workitems():
    WorkItems.find()
