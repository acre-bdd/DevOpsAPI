from DevOpsAPI import Wit, Step


def test_list_projects(api):
    print(api.Projects.list())
