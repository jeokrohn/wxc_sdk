from collections.abc import Generator
from typing import Optional, Literal

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..base import SafeEnum as Enum
from ..common import PersonPlaceAgent

__all__ = ['CallPickup', 'PickupNotificationType', 'CallPickupApi']


class PickupNotificationType(str, Enum):
    #: Notification is not sent to any member of the call pickup group.
    none = 'NONE'
    #: When the notificationDelayTimerSeconds number of seconds has elapsed, play an audio notification for each call
    #: pickup group member.
    audio_only = 'AUDIO_ONLY'
    #: When the notificationDelayTimerSeconds number of seconds has elapsed, provide a visual notification to every
    #: call pickup group member.
    visual_only = 'VISUAL_ONLY'
    #: When the notificationDelayTimerSeconds number of seconds has elapsed, provide a audio and visual notification to
    #: every call pickup group member.
    audio_and_visual = 'AUDIO_AND_VISUAL'


class CallPickup(ApiModel):
    #: A unique identifier for the call pickup.
    pickup_id: Optional[str] = Field(alias='id', default=None)
    #: Unique name for the call pickup. The maximum length is 80.
    name: Optional[str] = None
    #: Name of location for call pickup.
    location_name: Optional[str] = None
    #: ID of location for call pickup.
    location_id: Optional[str] = None
    #: Type of the notification when an incoming call is unanswered, the call pickup group notifies all of its members.
    notification_type: Optional[PickupNotificationType] = None
    #: After the number of seconds given by the notificationDelayTimerSeconds has elapsed, notify every member of the
    #: call pickup group when an incoming call goes unanswered. The notificationType field specifies the notification
    #: method.
    notification_delay_timer_seconds: Optional[int] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[PersonPlaceAgent]] = None

    def create_or_update(self) -> dict:
        """
        Get JSON for create or update call

        :return: JSON
        :rtype: str
        :meta private:
        """
        data = self.model_dump(mode='json',
                               by_alias=True,
                               exclude_none=True,
                               exclude={'pickup_id': True,
                                        'location_name': True,
                                        'location_id': True})
        # for create or update 'agents' is just a list of agent IDs
        if agents := data.pop('agents', None):
            data['agents'] = [a.pop('id', None) for a in agents]
        return data


class CallPickupApi(ApiChild, base='telephony/config/callPickups'):
    """
    Call Pickup API
    """

    def _endpoint(self, *, location_id: str, pickup_id: str = None, path: str = None) -> str:
        """
        call park specific feature endpoint like /v1/telephony/config/locations/{locationId}/callPickups/{pickup_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param pickup_id: call pickup id
        :type pickup_id: str
        :param path: addtl. path
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        pickup_id = pickup_id and f'/{pickup_id}' or ''
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/callPickups{pickup_id}{path}')
        return ep

    def list(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> Generator[CallPickup, None, None]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving this list requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :return: yields :class:`CallPickup` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallPickup, params=params, item_key='callPickups')

    def create(self, location_id: str, settings: CallPickup, org_id: str = None) -> str:
        """
        Create a Call Pickup

        Create new Call Pickups for the given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Creating a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param settings: settings for new call pickup
        :type settings: :class:`CallPickup`
        :param org_id: Create the call pickup for this organization.
        :return: ID of the newly created call pickup.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.create_or_update()
        data = self.post(url, json=body, params=params)
        return data['id']

    def delete_pickup(self, location_id: str, pickup_id: str, org_id: str = None):
        """
        Delete a Call Pickup

        Delete the designated Call Pickup.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Deleting a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param pickup_id: Delete the call pickup with the matching ID.
        :type pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url, params=params)

    def details(self, location_id: str, pickup_id: str, org_id: str = None) -> CallPickup:
        """
        Get Details for a Call Pickup

        Retrieve Call Pickup details.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving call pickup details requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str
        :return: call pickup info
        :rtype: :class:`CallPickup`
        """
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        params = org_id and {'orgId': org_id} or None
        return CallPickup.model_validate(self.get(url, params=params))

    def update(self, location_id: str, pickup_id: str, settings: CallPickup, org_id: str = None) -> str:
        """
        Update a Call Pickup

        Update the designated Call Pickup.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Updating a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param pickup_id: Update settings for a call pickup with the matching ID.
        :type pickup_id: str
        :param settings: updates
        :type settings: :class:`CallPickup`
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        body = settings.create_or_update()
        data = self.put(url, json=body, params=params)
        return data['id']

    def available_agents(self, location_id: str, call_pickup_name: str = None, name: str = None,
                         phone_number: str = None, order: str = None,
                         org_id: str = None) -> Generator[PersonPlaceAgent, None, None]:
        """
        Get available agents from Call Pickups
        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full, user, or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
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
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')
