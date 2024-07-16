# Tracking available numbers methods for users, virtual lines and workspaces

| Method                                     | Virtual Lines | Workspaces | User |
|--------------------------------------------|---------------|------------|------|
| GET Call Forward Available Phone Numbers   | X             | X          | X    |
| GET ECBN Available Phone Numbers           | X             | X          | X    |
| GET Fax Message Available Phone Numbers    | X             |            | X    | 
| GET Available Phone Numbers                | X             | X          |      |
| Get Call Intercept Available Phone Numbers |               | X          | X    |
| GET Primary Available Phone Numbers        |               |            | X    |
| GET Secondary Available Phone Numbers      |               |            | X    |

Virtual Lines

    Get Virtual Line Fax Message Available Phone Numbers [GET /telephony/config/virtualLines/{virtualLineId}/faxMessage/availableNumbers{?orgId,max,start,phoneNumber}]
    Get Virtual Line Call Forward Available Phone Numbers [GET /telephony/config/virtualLines/{virtualLineId}/callForwarding/availableNumbers{?orgId,max,start,phoneNumber,ownerName,extension}]
    Get Virtual Line ECBN Available Phone Numbers [GET /telephony/config/virtualLines/{virtualLineId}/emergencyCallbackNumber/availableNumbers{?orgId,max,start,phoneNumber,ownerName}]
    Get Virtual Line Available Phone Numbers [GET /telephony/config/virtualLines/availableNumbers{?orgId,locationId,max,start,phoneNumber}]

Workspaces

    Get Workspace Call Forward Available Phone Numbers [GET /telephony/config/workspaces/{workspaceId}/callForwarding/availableNumbers{?orgId,max,start,phoneNumber,ownerName,extension}]
    Get Workspace ECBN Available Phone Numbers [GET /telephony/config/workspaces/{workspaceId}/emergencyCallbackNumber/availableNumbers{?orgId,max,start,phoneNumber,ownerName}]
    Get Workspace Available Phone Numbers [GET /telephony/config/workspaces/availableNumbers{?orgId,locationId,max,start,phoneNumber}]
    Get Workspace Call Intercept Available Phone Numbers [GET /telephony/config/workspaces/{workspaceId}/callIntercept/availableNumbers{?orgId,max,start,phoneNumber,ownerName,extension}]

User/Person 

    Get Person Fax Message Available Phone Numbers [GET /telephony/config/people/{personId}/faxMessage/availableNumbers{?orgId,max,start,phoneNumber}]
    Get Person Call Forward Available Phone Numbers [GET /telephony/config/people/{personId}/callForwarding/availableNumbers{?orgId,max,start,phoneNumber,ownerName,extension}]
    Get Person ECBN Available Phone Numbers [GET /telephony/config/people/{personId}/emergencyCallbackNumber/availableNumbers{?orgId,max,start,phoneNumber,ownerName}]
    Get Person Call Intercept Available Phone Numbers [GET /telephony/config/people/{personId}/callIntercept/availableNumbers{?orgId,max,start,phoneNumber,ownerName,extension}]
    Get Person Primary Available Phone Numbers [GET /telephony/config/people/primary/availableNumbers{?orgId,locationId,max,start,phoneNumber,licenseType}]
    Get Person Secondary Available Phone Numbers [GET /telephony/config/people/{personId}/secondary/availableNumbers{?orgId,max,start,phoneNumber}]
