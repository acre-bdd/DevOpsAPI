# DevOpsAPI
> A simple object-oriented easy-to-use python inteface to the Azure DevOps REST API

## Features

-   Create, Delete and Modify WorkItems and Test Cases
-   Query WorkItems using the wsql


## Quickstart

-   Create an PAT on DevOps, give permissions for the scopes you want to
    access


        from DevOpsAPI import Api, Wit, Step

        api = Api(organisation="myorg",
                  projet="myproject",
                  user="your@email.com",
                  apikey="PAT")

-    Create a WorkItem

         wi = api.WorkItem.create(type=Wit.Task,
                                  title="First Task",
                                  area="my\\area")
         wi.Description = "Describe your Task"
         wi.Tags = "tag1,tag2"

-    Create a Test Case

         wi = api.TestCase.create(title="First TestCase",
                                 area="my\\area")
         wi.Description = "Describe your Test Case"
         wi.Tags = "tag1,tag2"
        
-    Add some Steps to the Test Case

         step1 = Step("Given I use DevOpsAPI")
         step2 = Step("Then I am happy")
         wi.Steps = [step1, step2]

