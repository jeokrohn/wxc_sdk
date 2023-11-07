from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateACallPickupResponse', 'GetAvailableAgentsFromCallPickupsResponse', 'GetCallPickupObject',
            'GetPersonPlaceVirtualLineCallPickupObject', 'GetPersonPlaceVirtualLineCallPickupObjectType',
            'GetUserNumberItemObject', 'ListCallPickupObject', 'ModifyCallPickupObject',
            'ReadTheListOfCallPickupsResponse']


class GetPersonPlaceVirtualLineCallPickupObjectType(str, Enum):
    #: Indicates that this object is a user.
    people = 'PEOPLE'
    #: Indicates that this object is a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person or workspace.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of a person or workspace.
    #: example: 8080
    extension: Optional[datetime] = None
    #: Flag to indicate a primary phone.
    #: example: True
    primary: Optional[bool] = None


class GetPersonPlaceVirtualLineCallPickupObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: First name of a person, workspace or virtual line.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    #: example: Brown
    last_name: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    #: example: johnBrown
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[GetPersonPlaceVirtualLineCallPickupObjectType] = None
    #: Email of a person, workspace or virtual line.
    #: example: john.brown@example.com
    email: Optional[str] = None
    #: List of phone numbers of a person, workspace or virtual line.
    phone_number: Optional[list[GetUserNumberItemObject]] = None


class GetCallPickupObject(ApiModel):
    #: A unique identifier for the call pickup.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUElDS1VQL1kyRnNiRkJwWTJ0MWNERT0
    id: Optional[str] = None
    #: Unique name for the call pickup. The maximum length is 80.
    #: example: North Alaska-Group
    name: Optional[str] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]] = None


class ListCallPickupObject(ApiModel):
    #: Unique name for the call pickup. The maximum length is 80.
    #: example: North Alaska-Group
    name: Optional[str] = None
    #: A unique identifier for the call pickup.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUElDS1VQL1kyRnNiRkJwWTJ0MWNERT0
    id: Optional[str] = None
    #: Name of the location for call pickup.
    #: example: Alaska
    location_name: Optional[str] = None
    #: ID of the location for call pickup.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class ModifyCallPickupObject(ApiModel):
    #: Unique name for the call pickup. The maximum length is 80.
    #: example: North Alaska-Group
    name: Optional[str] = None
    #: An array of people, workspace, and virtual lines IDs, that are added to call pickup.
    agents: Optional[list[str]] = None


class ReadTheListOfCallPickupsResponse(ApiModel):
    #: Array of call pickups.
    call_pickups: Optional[list[ListCallPickupObject]] = None


class CreateACallPickupResponse(ApiModel):
    #: ID of the newly created call pickup.
    id: Optional[str] = None


class GetAvailableAgentsFromCallPickupsResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]] = None


class FeaturesCallPickupApi(ApiChild, base='telephony/config/locations/{locationId}/callPickups'):
    """
    Features:  Call Pickup
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Call Pickup supports reading and writing of Webex Calling Call Pickup settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """
    ...