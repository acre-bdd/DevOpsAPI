from DevOpsAPI import Wit


def test_create_get_delete(api, area):
    wi2 = api.WorkItem.create(Wit.Task, "this is a task", area=area)
    assert wi2.id > 0
    assert wi2.Title == "this is a task"
    wi = api.WorkItem.get(wi2.id)
    assert wi.id == wi2.id
    assert wi.Title == "this is a task"
    wi.delete()


def test_modify(api, area):
    wi = api.WorkItem.create(Wit.Task, "modify task", area=area)
    wi.Description = "description1"
    assert wi.Title == "modify task"
    assert wi.Description == "description1"
    wi.Title = "modified task title"
    wi.Description = "description2"
    wi2 = api.WorkItem.get(wi.id)
    assert wi2.Title == "modified task title"
    assert wi2.Description == "description2"
    wi.delete()


def test_find(api, area):
    ids = api.WorkItems.find({"System.WorkItemType": Wit.Task})
    for id in ids:
        api.WorkItem.get(id=id).delete()
    wi1 = api.WorkItem.create(Wit.Task, "list task 1", area=area)
    wi2 = api.WorkItem.create(Wit.Task, "list task 2", area=area)
    wi3 = api.WorkItem.create(Wit.Task, "list task 3", area=area)
    ids = api.WorkItems.find({"System.WorkItemType": Wit.Task})
    assert len(ids) == 3
    assert wi1.id in ids
    assert wi1.id in ids
    assert wi2.id in ids
    assert wi3.id in ids
