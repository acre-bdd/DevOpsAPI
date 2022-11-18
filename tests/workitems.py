from DevOpsApi import Api, Wit

api = Api(organization="ck0548",
          project="acre",
          user="ck@realtime-projects.com",
          apikey="hctd4coz47i4qc6pd3dl5wml6dwf4jio5hqc44ykafrf3zv7khsa")


def test_create_get_delete():

    wi2 = api.WorkItem.create(Wit.Task, "this is a task", area="acre\\pytest")
    assert wi2.id > 0
    assert wi2.Title == "this is a task"
    wi = api.WorkItem.get(wi2.id)
    assert wi.id == wi2.id
    assert wi.Title == "this is a task"
    wi.delete()


def test_modify():
    wi = api.WorkItem.create(Wit.Task, "modify task", area="acre\\pytest")
    assert wi.Title == "modify task"
    wi.Title = "modified task title"
    assert wi.Title == "modified task title"
    wi.delete()


def test_find():
    ids = api.WorkItems.find({"System.WorkItemType": Wit.Task})
    for id in ids:
        api.WorkItem.get(id=id).delete()
    wi1 = api.WorkItem.create(Wit.Task, "list task 1", area="acre\\pytest")
    wi2 = api.WorkItem.create(Wit.Task, "list task 2", area="acre\\pytest")
    wi3 = api.WorkItem.create(Wit.Task, "list task 3", area="acre\\pytest")
    ids = api.WorkItems.find({"System.WorkItemType": Wit.Task})
    assert len(ids) == 3
    assert wi1.id in ids
    assert wi1.id in ids
    assert wi2.id in ids
    assert wi3.id in ids
