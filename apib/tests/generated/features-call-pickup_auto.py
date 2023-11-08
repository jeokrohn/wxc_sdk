from collections.abc import Generator
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

    def read_the_list_of_call_pickups(self, location_id: str, org_id: str = None, max_: int = None, start: int = None,
                                      order: str = None, name: str = None,
                                      **params) -> Generator[ListCallPickupObject, None, None]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.
        
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        
        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.
        
        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :param max_: Limit the number of call pickups returned to this maximum count. Default is 2000.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching call pickups. Default is 0.
        :type start: int
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :return: Generator yielding :class:`ListCallPickupObject` instances
        """
        ...


    def create_a_call_pickup(self, location_id: str, name: str, agents: list[str], org_id: str = None) -> str:
        """
        Create a Call Pickup

        Create new Call Pickups for the given location.
        
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        
        Creating a call pickup requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.
        
        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param agents: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
        :type agents: list[str]
        :param org_id: Create the call pickup for this organization.
        :type org_id: str
        :rtype: str
        """
        ...


    def delete_a_call_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None):
        """
        Delete a Call Pickup

        Delete the designated Call Pickup.
        
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        
        Deleting a call pickup requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.
        
        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param call_pickup_id: Delete the call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str
        :rtype: None
        """
        ...


    def get_details_for_a_call_pickup(self, location_id: str, call_pickup_id: str,
                                      org_id: str = None) -> GetCallPickupObject:
        """
        Get Details for a Call Pickup

        Retrieve Call Pickup details.
        
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        
        Retrieving call pickup details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.
        
        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param call_pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallPickupObject`
        """
        ...


    def update_a_call_pickup(self, location_id: str, call_pickup_id: str, name: str, agents: list[str],
                             org_id: str = None) -> str:
        """
        Update a Call Pickup

        Update the designated Call Pickup.
        
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        
        Updating a call pickup requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.
        
        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param call_pickup_id: Update settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param agents: An array of people, workspace, and virtual lines IDs, that are added to call pickup.
        :type agents: list[str]
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        :rtype: str
        """
        ...


    def get_available_agents_from_call_pickups(self, location_id: str, org_id: str = None,
                                               call_pickup_name: str = None, max_: int = None, start: int = None,
                                               name: str = None, phone_number: str = None, order: str = None,
                                               **params) -> Generator[GetPersonPlaceVirtualLineCallPickupObject, None, None]:
        """
        Get available agents from Call Pickups

        Retrieve available agents from call pickups for a given location.
        
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        
        Retrieving available agents from call pickups requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param max_: Limit the number of available agents returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching available agents.
        :type start: int
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: `fname`, `lname`, `extension`,
            `number`.
        :type order: str
        :return: Generator yielding :class:`GetPersonPlaceVirtualLineCallPickupObject` instances
        """
        ...

    ...