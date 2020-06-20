## About the tool

The DLRS is a tool that offers a feature set that extends a feature called "rollup summaries" on the Salesforce platform. It deploys Apex code to your organization and enables administrators to deploy automatically generated code to the org (even a production environment, yes).

The tool code operates using custom metadata records managed by a Visualforce page on the project. From there an administrator or a developer can create custom metadata records for the tool to use when running its triggers (the code deployed which was mentioned before).

When a record with a DLRS trigger is saved, it activates the DLRS tool which then gets the custom setting for the specific object. Then it queries the object and its related record(s) to update its rollup summary.

### Example

A rollup is created on Custom Object A (`CustomObjectA__c`) to count how many Custom Object B's (`CustomObjectB__c`) records are related to it through a common lookup field (not a master-detail relationship, that is).

When a new object B is created, updated or deleted, the tool analyzes the criteria defined on its custom setting (the custom metadata type) and evaluates whether or not to update the counter on the parent (object A) field.
