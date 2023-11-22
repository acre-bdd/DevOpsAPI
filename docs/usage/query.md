# Querying Work Items

DevOpsAPI offers a simplified interface for querying work items.

The `api.WorkItems.find()` function takes a dicitionary of attributes
to query for and returns a list of _Work Item Ids_ of Work Items that
match the attribute specification:

``` python
from DevOpsAPI import Api, Wit
api = Api(...)
query = {
    "System.WorkItemType": Wit.TestCase,
    "System.AreaPath": {"UNDER": "area\\path"}
}
ids = self.api.WorkItems.find(query)
```

## Operators

Like in the example above, use can supply a dictionary as value
specifying the operator for the attribute query:

``` python
query = {
    "System.WorkItemType": Wit.TestCase,
    "System.Title": {"Does not Contain": title}
}
```

## Contains

If the value starts witha `~`, the query will automaticaly use the `Contains` operator.
Both queries will produce the same result:

``` python
query1 = {"System.Title": {"Contains": "My Title"}
query2 = {"System.Title": "~My Title"}
```
