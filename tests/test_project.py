
def test_list_projects(api):
    projects = api.Projects.list()
    assert len(projects) > 0
