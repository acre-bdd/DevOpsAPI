from .wi import WorkItem, WorkItems, Wit
from .connection import Connection


class Api:
    def __init__(self, organization, project, user, apikey):
        self._connection = Connection(organization, project, user, apikey)

    @property
    def WorkItem(self):
        return WorkItem(self._connection)

    @property
    def WorkItems(self):
        return WorkItems(self._connection)
