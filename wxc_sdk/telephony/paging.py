"""
Paging group API

"""
from ..api_child import ApiChild
from collections.abc import Generator
from ..base import ApiModel, to_camel
from pydantic import Field
from typing import Optional, List, Union
from .user_base import UserType

__all__ = ['PagingAPI', 'Paging']


class Agent(ApiModel):
    #: Agents ID
    agent_id: str = Field(alias='id')
    #: Agents first name. Minimum length is 1. Maximum length is 30.
    first_name: str
    #: Agents last name. Minimum length is 1. Maximum length is 30.
    last_name: str
    #: Type of the person or workspace.
    agent_type: UserType = Field(alias='type')
    #: Agents phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Agents extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    extension: Optional[str]


IdOrAgent = Union[str, Agent]


class Paging(ApiModel):
    #: A unique identifier for the paging group.
    paging_id: Optional[str] = Field(alias='id')
    #: Whether or not the paging group is enabled.
    enabled: Optional[bool]
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    name: str
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is
    #: mandatory.
    phone_number: Optional[str]
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    # TODO: raise documentation issue
    #: is the phone numer a toll free number?
    toll_free_number: Optional[bool]
    #: Paging language. Minimum length is 1. Maximum length is 40.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator
    #: ID.
    originator_caller_id_enabled: Optional[bool]
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    #: When creating a paging group then this is a list of agent IDs. The details() call returns detailed agent
    #: information
    originators: Optional[List[IdOrAgent]]
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[List[IdOrAgent]]
    #: Name of location for paging group. Only present in list() response.
    #: When creating a paging group then this is a list of agent IDs. The details() call returns detailed agent
    #: information
    location_name: Optional[str]
    #: ID of location for paging group. Only present in list() response.
    location_id: Optional[str]


class PagingAPI(ApiChild, base='telephony/config'):

    def _endpoint(self, *, location_id: str = None, paging_id: str = None) -> str:
        """
        endpoint for paging group operation

        :meta private:
        :param location_id:
        :type location_id: str
        :param paging_id:
        :type paging_id: str
        """
        if location_id is None:
            return super().ep('paging')
        paging_id = paging_id and f'/{paging_id}' or ''
        return super().ep(f'locations/{location_id}/paging{paging_id}')

    def list(self, *, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None) -> Generator[Paging, None, None]:
        """
        Read the List of Paging Groups
        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List paging groups for this organization.
        :type org_id: str
        :return: generator of class:`Paging` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self._endpoint()
        return self.session.follow_pagination(url=url, model=Paging, params=params, item_key='locationPaging')
        pass

    def create(self, *, location_id: str, paging: Paging, org_id: str = None) -> str:
        """
        Create a new Paging Group
        Create a new Paging Group for the given location.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Creating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the paging group for this location.
        :type location_id: str
        :param paging: new paging group
        :type paging: Paging
        :param org_id: Create the paging group for this organization.
        :type org_id: str
        :return: ID of the newly created paging group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        paging_data = paging.json(exclude={'paging_id', 'location_name', 'location_id'})
        data = self.post(url, data=paging_data, params=params)
        return data['id']

    def delete_paging(self, *, location_id: str, paging_id: str, org_id: str = None):
        """
        Delete a Paging Group
        Delete the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Deleting a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a paging group.
        :type location_id: str
        :param paging_id: Delete the paging group with the matching ID.
        :param org_id: Delete the paging group from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        self.delete(url, params=params)

    def details(self, *, location_id: str, paging_id: str, org_id: str = None) -> Paging:
        """
        Get Details for a Paging Group
        Retrieve Paging Group details.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving paging group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        :param location_id: Retrieve settings for a paging group in this location.
        :param paging_id: Retrieve settings for the paging group with this identifier.
        :param org_id: Retrieve paging group settings from this organization.
        :return: :class:`Paging` object
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        return Paging.parse_obj(self.get(url, params=params))

    def update(self, *, location_id: str, update: Paging, paging_id: str, org_id: str = None):
        """
        Update the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Updating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update settings for a paging group in this location.
        :type location_id: str
        :param update: update parameters
        :type update: Paging
        :param paging_id: Update settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Update paging group settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        paging = update.copy(deep=True)
        # for update originators and targets are just the IDs
        if paging.originators is not None:
            paging.originators = [o.agent_id if isinstance(o, Agent) else o for o in paging.originators]
        if paging.targets is not None:
            paging.targets = [t.agent_id if isinstance(t, Agent) else t for t in paging.targets]
        paging_data = paging.json()
        self.put(url, data=paging_data, params=params)
