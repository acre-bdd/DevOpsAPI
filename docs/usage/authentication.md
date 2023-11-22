# Setup

## Personal Access Token

In order to access and control the _DevOps REST API_ interface, a _personal access token_
is required for authentication. Follow 
[these instructions](https://tinyurl.com/3ssc25vf) to create your personal access token.

## Creating the api instance

In order to connect to the REST API services, you furthermore need the following
information:

-   The **organization name** where your project is hosted
-   The **project name** of your project
-   The **email address** of the user for which you created the personal access token

Given you have all this information, you can create an instance of the `DevOpsApi.Api` class
which you can then use to read and modify elements using the DevOpsAPI REST service:


``` python
from DevOpsAPI import Api, Wit, Step

api = Api(organisation="myorg",
          project="myproject",
          user="your@email.com",
          apikey="PAT")
```

## Further reading

-   [Querying work items](query.md)
