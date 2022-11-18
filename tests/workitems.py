from DevOpsApi.wi import WorkItem, WorkItems, Wit


def test_create_get_workitem():
    wi2 = WorkItem.create(Wit.Task, "this is a task", area="acre\\pytest")
    assert wi2.id > 0
    assert wi2.title == "this is a task"
    wi = WorkItem.get(wi2.id)
    assert wi.id == wi2.id
    assert wi.title == "this is a task"
    wi.delete()


def test_list_workitems():
    WorkItems.find()
