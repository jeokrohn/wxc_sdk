import json
from collections.abc import Generator
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum
from ..common import RingPattern, PersonPlaceAgent, CallParkExtension

__all__ = ['CallParkRecall', 'RecallHuntGroup', 'AvailableRecallHuntGroup',
           'CallPark', 'CallParkSettings', 'LocationCallParkSettings', 'CallParkApi']


class CallParkRecall(str, Enum):
    #: Alert parking user only.
    parking_user_only = 'ALERT_PARKING_USER_ONLY'
    #: Alert parking user first, then hunt group.
    parking_user_first_then_hunt_group = 'ALERT_PARKING_USER_FIRST_THEN_HUNT_GROUP'
    #: Alert hunt group only.
    hunt_group_only = 'ALERT_HUNT_GROUP_ONLY'


class RecallHuntGroup(ApiModel):
    #: Alternate user which is a hunt group id for call park recall alternate destination.
    hunt_group_id: Optional[str] = None
    #: Unique name for the hunt group.
    hunt_group_name: Optional[str] = None
    #: Call park recall option.
    option: Optional[CallParkRecall] = None

    @staticmethod
    def default() -> 'RecallHuntGroup':
        """
        Default recall: parking user only, no hunt group

        :return: :class:`RecallHuntGroup` object
        :rtype: :class:`RecallHuntGroup`
        """
        return RecallHuntGroup(option=CallParkRecall.parking_user_only)


class AvailableRecallHuntGroup(ApiModel):
    """
    available recall hunt group
    """
    #: A unique identifier for the hunt group.
    huntgroup_id: str = Field(alias='id')
    #: Unique name for the hunt group.
    name: str


class CallPark(ApiModel):
    """
    Call Park
    """
    #: A unique identifier for the call park.
    callpark_id: Optional[str] = Field(alias='id', default=None)
    #: Unique name for the call park. The maximum length is 80.
    name: Optional[str] = None
    #: Name of location for call park
    location_name: Optional[str] = None
    #: ID of location for call park.
    location_id: Optional[str] = None
    #: Recall options that are added to call park.
    recall: Optional[RecallHuntGroup] = None
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[PersonPlaceAgent]] = None
    #: Whether or not the calls will be parked on agents as a destination.
    park_on_agents_enabled: Optional[bool] = None
    #: Array of call park extensions assigned to a call park.
    call_park_extensions: Optional[list[CallParkExtension]] = None

    @staticmethod
    def default(*, name: str) -> 'CallPark':
        """
        Default (trivial) call park group

        no agents, recall to parking user only

        :param name: call park group name
        :type name: str
        :return: :class:`CallPark` instance
        :rtype: :class`CallPark`
        """
        return CallPark(name=name, recall=RecallHuntGroup.default())

    def create_or_update(self) -> str:
        """
        Get JSON for create or update call

        :return: JSON
        :rtype: str
        """
        data = self.model_dump(mode='json', exclude_unset=True,
                               exclude={'callpark_id': True,
                                        'location_name': True,
                                        'location_id': True,
                                        'recall': {'hunt_group_name': True}})
        # agents need to be passed as list of IDs only
        if data.get('agents'):
            data['agents'] = [a['id'] for a in data['agents']]
        # callParkExtensions need to be passed as list of IDs only
        if data.get('callParkExtensions'):
            data['callParkExtensions'] = [a['id'] for a in data['callParkExtensions']]

        return json.dumps(data)


class CallParkSettings(ApiModel):
    """
    Setting controlling call park behavior.
    """
    #: Ring pattern for when this callpark is called.
    ring_pattern: Optional[RingPattern] = None
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up within the
    #: set time, then the call will be recalled based on the Call Park Recall setting.
    recall_time: Optional[int] = None
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up, the call
    #: will revert back to the hunt group (after the person who parked the call is alerted).
    hunt_wait_time: Optional[int] = None

    @staticmethod
    def default() -> 'CallParkSettings':
        """
        Default call park settings

        :return: :class:`CallParkSettings`
        """
        return CallParkSettings(ring_pattern=RingPattern.normal,
                                recall_time=45,
                                hunt_wait_time=45)


class LocationCallParkSettings(ApiModel):
    #: Recall options that are added to call park.
    call_park_recall: Optional[RecallHuntGroup] = None
    #: Setting controlling call park behavior.
    call_park_settings: Optional[CallParkSettings] = None

    @staticmethod
    def default() -> 'LocationCallParkSettings':
        """
        Default location call park settings

        :return: :class:`LocationCallParkSettings`
        """
        return LocationCallParkSettings(call_park_recall=RecallHuntGroup.default(),
                                        call_park_settings=CallParkSettings.default())

    def update(self) -> str:
        """
        Get JSON for update call

        :return: JSON
        :rtype: str
        """
        return self.model_dump_json(exclude={'call_park_recall': {'hunt_group_name': True}})


class CallParkApi(ApiChild, base='telephony/config/callParks'):
    """
    Features:  Call Park

    Features: Call Park supports reading and writing of Webex Calling Call Park settings for a specific organization.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def _endpoint(self, *, location_id: str, callpark_id: str = None, path: str = None) -> str:
        """
        call park specific feature endpoint like /v1/telephony/config/locations/{locationId}/callParks/{callpark_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param callpark_id: call park id
        :type callpark_id: str
        :param path: addtl. path
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        call_park_id = callpark_id and f'/{callpark_id}' or ''
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/callParks{call_park_id}{path}')
        return ep

    def list(self, location_id: str, order: str = None, name: str = None,
             org_id: str = None, **params) -> Generator[CallPark, None, None]:
        """
        Read the List of Call Parks

        List all Call Parks for the organization.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :return: yields :class:`CallPark` objects
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallPark, params=params, item_key='callParks')

    def create(self, location_id: str, settings: CallPark, org_id: str = None) -> str:
        """
        Create a Call Park Extension

        Create new Call Park Extensions for the given location.

        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.

        Creating a call park extension requires a full administrator or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Create the call park for this location.
        :type location_id: str
        :param settings: settings for new call park
        :type settings: :class:`CallPark`
        :param org_id: Create the call park for this organization.
        :return: ID of the newly created call park.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.create_or_update()
        data = self.post(url, data=body, params=params)
        return data['id']

    def delete_callpark(self, location_id: str, callpark_id: str, org_id: str = None):
        """
        Delete a Call Park

        Delete the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Deleting a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location from which to delete a call park.
        :type location_id: str
        :param callpark_id: Delete the call park with the matching ID.
        :type callpark_id: str
        :param org_id: Delete the call park from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url, params=params)

    def details(self, location_id: str, callpark_id: str, org_id: str = None) -> CallPark:
        """
        Get Details for a Call Park

        Retrieve Call Park details.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving call park details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Retrieve settings for a call park in this location.
        :type location_id: str
        :param callpark_id: Retrieve settings for a call park with the matching ID.
        :type callpark_id: str
        :param org_id: Retrieve call park settings from this organization.
        :type org_id: str
        :return: call park info
        :rtype: :class:`CallPark`
        """
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        params = org_id and {'orgId': org_id} or None
        return CallPark.model_validate(self.get(url, params=params))

    def update(self, location_id: str, callpark_id: str, settings: CallPark, org_id: str = None) -> str:
        """
        Update a Call Park

        Update the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: RLocation in which this call park exists.
        :type location_id: str
        :param callpark_id: Update settings for a call park with the matching ID.
        :type callpark_id: str
        :param settings: updates
        :type settings: :class:`CallPark`
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        body = settings.create_or_update()
        data = self.put(url, data=body, params=params)
        return data['id']

    def available_agents(self, location_id: str, call_park_name: str = None, name: str = None, phone_number: str = None,
                         order: str = None, org_id: str = None, **params) -> Generator[PersonPlaceAgent, None, None]:
        """
        Get available agents from Call Parks

        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        if org_id is not None:
            params['orgId'] = org_id
        if call_park_name is not None:
            params['callParkName'] = call_park_name
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')

    def available_recalls(self, location_id: str, name: str = None, order: str = None,
                          org_id: str = None, **params) -> Generator[AvailableRecallHuntGroup, None, None]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth
        token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort
            fields: lname.
        :param order: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :return: yields :class:`AvailableRecallHuntGroup` objects
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self._endpoint(location_id=location_id, path='availableRecallHuntGroups')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AvailableRecallHuntGroup,
                                              params=params, item_key='huntGroups')

    def call_park_settings(self, location_id: str, org_id: str = None) -> LocationCallParkSettings:
        """
        Get Call Park Settings

        Retrieve Call Park Settings from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving settings from call parks requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Return the call park settings for this location.
        :type location_id: str
        :param org_id: Return the call park settings for this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='settings')
        return LocationCallParkSettings.model_validate(self.get(url, params=params))

    def update_call_park_settings(self, location_id: str, settings: LocationCallParkSettings, org_id: str = None):
        """
        Update Call Park settings

        Update Call Park settings for the designated location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating call park settings requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location for which call park settings will be updated.
        :type location_id: str
        :param settings: update settings
        :type settings: :class:`LocationCallParkSettings`
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='settings')
        body = settings.update()
        self.put(url, params=params, data=body)
