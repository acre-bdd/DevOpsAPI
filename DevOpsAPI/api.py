from .wi import WorkItem, WorkItems, TestCase
from .testing import TestRun, TestResults, TestRuns, TestPlans
from .wi import Wit, Step  # noqa: F401
from .projects import Projects, Project  # noqa: F401
from .connection import Connection


class Api:
    def __init__(self, organization, project, user, apikey):
        self._connection = Connection(organization, project, user, apikey)

    @property
    def WorkItem(self):
        return WorkItem(self._connection)

    @property
    def TestCase(self):
        return TestCase(self._connection)

    @property
    def TestCases(self):
        return TestCase(self._connection)

    @property
    def WorkItems(self):
        return WorkItems(self._connection)

    @property
    def TestRun(self):
        return TestRun(self._connection)

    @property
    def TestRuns(self):
        return TestRuns(self._connection)

    @property
    def TestResults(self):
        return TestResults(self._connection)

    @property
    def TestPlans(self):
        return TestPlans(self._connection)

    @property
    def Projects(self):
        return Projects(self._connection)
