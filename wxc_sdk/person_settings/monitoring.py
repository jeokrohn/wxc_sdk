"""
call monitoring API
"""

from collections.abc import Generator
from typing import Any, Optional

from pydantic import Field

from ..base import ApiModel, webex_id_to_uuid
from ..common import IdAndName, MonitoredMember, UserType
from .common import PersonSettingsApiChild

__all__ = [
    'MonitoredElementMember',
    'MonitoredElementSpeedDial',
    'MonitoredElementCPE',
    'Monitoring',
    'MonitoringMember',
    'MonitoringApi',
]


class MonitoredElementMember(MonitoredMember):
    # the location name
    location: str
    #: The location ID for the location.
    location_id: Optional[str] = None
    #: This is a custom line key label configured for the monitored member.
    line_key_label: Optional[str] = None

    @property
    def ci_location_id(self) -> Optional[str]:
        return self.location_id and webex_id_to_uuid(self.location_id)


class MonitoredElementSpeedDial(ApiModel):
    #: ID of the configured speed dial (person or workspace or virtual line).
    id: Optional[str] = None
    #: First name of the monitored speed dial item (virtual line or person). For a workspace, this field is not
    #: applicable.
    first_name: Optional[str] = None
    #: Last name of the monitored speed dial item (virtual line or person). For a workspace, this field is not
    #: applicable.
    last_name: Optional[str] = None
    #: Display name of the configured speed dial (person or workspace or virtual line).
    display_name: Optional[str] = None
    #: Indicates whether type is person, workspace, or virtual line.
    type: Optional[UserType] = None
    #: Primary phone number for the configured speed dial. It can be either a person, workspace or virtual line. In
    #: case of a custom speed dial, it can be any external phone number.
    phone_number: Optional[str] = None
    #: Primary extension for the configured speed dial. It can be either of a person or workspace or virtual line.
    extension: Optional[str] = None
    #: This is a custom line key label configured for the speed dial on the device.
    line_key_label: Optional[str] = None
    #: Name of the location for the call park.
    location: Optional[str] = None
    #: ID of the location for the call park.
    location_id: Optional[str] = None


class MonitoredElementCPE(ApiModel):
    #: The identifier of the call park extension.
    id: Optional[str] = None
    #: The name used to describe the call park extension.
    name: Optional[str] = None
    #: This is a custom line key label configured for the Call Park Extension.
    line_key_label: Optional[str] = None
    #: The extension number for the call park extension.
    extension: Optional[str] = None
    #: Routing prefix of the location.
    routing_prefix: Optional[str] = None
    #: Routing prefix plus extension of the Call Park Extension. If routing prefix is not configured for the location,
    #: esn will be same as extension.
    esn: Optional[str] = None
    #: The location name where the call park extension is.
    location: Optional[str] = None
    #: The ID of the location.
    location_id: Optional[str] = None


class MonitoredElement(ApiModel):
    #: Monitored person, workspace, or virtual line.
    member: Optional[MonitoredElementMember] = None
    #: Monitored call park extension.
    cpe: Optional[MonitoredElementCPE] = Field(alias='callparkextension', default=None)
    #: Speed dial configured as a monitored element.
    speed_dial: Optional[MonitoredElementSpeedDial] = None


class Monitoring(ApiModel):
    #: Call park notification is enabled or disabled.
    call_park_notification_enabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, or call park extension.
    #: for updates only the member IDs need to be set
    monitored_elements: Optional[list[MonitoredElement]] = None
    #: Indicates additional number of entries that can be stored (more than the number of entries listed).
    available_entries_count: Optional[int] = None

    @property
    def monitored_cpes(self) -> list[MonitoredElementCPE]:
        return [me.cpe for me in self.monitored_elements or [] if me.cpe]

    @property
    def monitored_members(self) -> list[MonitoredElementMember]:
        return [me.member for me in self.monitored_elements or [] if me.member]

    def update(self) -> dict[str, Any]:
        """
        data for update

        :meta private:
        :return:
        """
        data = self.model_dump(
            mode='json',
            by_alias=True,
            exclude_none=True,
            include={
                'monitored_elements': {
                    '__all__': {
                        'member': {'member_id': True, 'line_key_label': True},
                        'cpe': {'id': True, 'line_key_label': True},
                        'speed_dial': {'id': True, 'phone_number': True, 'line_key_label': True},
                    }
                },
            },
        )
        if self.monitored_elements:
            # update for each monitored element only has id, type, line_key_label, and phone_number (for speed dials)
            monitored_elements = []
            me_attr_to_type = {
                'member': 'MEMBER',
                'callparkextension': 'CALL_PARK_EXTENSION',
                'speedDial': 'SPEED_DIAL',
            }
            for me in data['monitoredElements']:
                # only one attribute is set: member, cpe, or speed_dial
                me_attr = next(iter(me))
                me_data = me[me_attr]
                me_data['type'] = me_attr_to_type[me_attr]
                monitored_elements.append(me_data)
            data['monitoredElements'] = monitored_elements
        # different attribute name in update
        if self.call_park_notification_enabled is not None:
            data['enableCallParkNotification'] = str(self.call_park_notification_enabled).lower()
        return data


class MonitoringMember(ApiModel):
    #: Unique identifier of the member (PEOPLE, PLACE or VIRTUAL_LINE resource type).
    id: Optional[str] = None
    #: First name of the member (virtual line or person). For a workspace, this field is not applicable.
    first_name: Optional[str] = None
    #: Last name of the member (virtual line or person). For a workspace, this field is not applicable.
    last_name: Optional[str] = None
    #: The display name of the monitored person, workspace, or virtual line.
    display_name: Optional[str] = None
    #: Phone number of the member.
    phone_number: Optional[str] = None
    #: Extension of the member.
    extension: Optional[str] = None
    type: Optional[UserType] = None
    #: Location details of the member.
    location: Optional[IdAndName] = None


class MonitoringApi(PersonSettingsApiChild):
    """
    API for person's call monitoring settings, also used for workspaces
    """

    feature = 'monitoring'

    def read(self, entity_id: str, org_id: str = None) -> Monitoring:
        """
        Retrieve an entity's Monitoring Settings

        Retrieves the monitoring settings of the entity, which shows specified people, places, virtual lines or call
        park extensions that are being monitored.

        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :return: monitoring settings
        :rtype: :class:`Monitoring`
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return Monitoring.model_validate(data)

    def configure(self, entity_id: str, settings: Monitoring, org_id: str = None):
        """
        Modify an entity's Monitoring Settings

        Modifies the monitoring settings of the entity.

        Monitors the line status of specified people, places, virtual lines or call park extension. The line status
        indicates if a person, place or virtual line is on a call and if a call has been parked on that extension.

        The number of monitored elements is limited to 50.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: settings for update
        :type settings: :class:`Monitoring`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.update()
        self.put(ep, params=params, json=data)

    def get_available_members_for_monitoring(
        self,
        entity_id: str,
        location_id: str = None,
        member_name: str = None,
        phone_number: str = None,
        order: list[str] = None,
        org_id: str = None,
        **params: Any,
    ) -> Generator[MonitoringMember, None, None]:
        """
        Get Available Members for Person or Workspace monitoring

        Get available members for person monitoring. This API allows administrators to retrieve a list of members that
        can be added to the monitoring list for a specific person or workspace

        Webex Calling monitoring allows a person to watch the line status of selected people, workspaces, and virtual
        lines. Configuring a monitoring list helps the person quickly see whether monitored members are on a call.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person or workspace.
        :type entity_id: str
        :param location_id: Search for the available members in the location ID.
        :type location_id: str
        :param member_name: Search for available members by name.
        :type member_name: str
        :param phone_number: Search for available members by number or extension.
        :type phone_number: str
        :param order: Sort response based on `firstName` or `lastName` with sort direction `asc` or `desc`. Example:
            `lastName-asc` or `firstName-desc`. Default sort is ascending order.
        :type order: list[str]
        :param org_id: ID of the organization within which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :return: Generator yielding :class:`MonitoringMember` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = ','.join(order)
        url = self.f_ep(entity_id, 'availableMembers')
        return self.session.follow_pagination(url=url, model=MonitoringMember, item_key='members', params=params)

    def get_available_speed_dials_for_monitoring(
        self,
        entity_id: str,
        location_id: str = None,
        member_name: str = None,
        phone_number: str = None,
        order: list[str] = None,
        org_id: str = None,
        **params: Any,
    ) -> Generator[MonitoringMember, None, None]:
        """
        Get Available Speed Dials for Person or Workspace Monitoring

        Get available speed dials for Person monitoring configuration. This API allows administrators to retrieve a
        list of members that can be added as speed dials for monitoring a specific person.

        Speed dials allow quick access to frequently contacted members. When configured for monitoring, speed dials
        enable users to quickly call or monitor the status of specific members within the organization.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person or workspace
        :type entity_id: str
        :param location_id: Search for the available speed dials in the location ID.
        :type location_id: str
        :param member_name: Search for available members by name.
        :type member_name: str
        :param phone_number: Search for available members by number or extension.
        :type phone_number: str
        :param order: Sort response based on `firstName` or `lastName` with sort direction `asc` or `desc`. Example:
            `lastName-asc` or `firstName-desc`. Default sort is ascending order.
        :type order: list[str]
        :param org_id: ID of the organization within which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :return: Generator yielding :class:`MonitoringMember` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = ','.join(order)
        url = self.f_ep(entity_id, 'speedDials/availableMembers')
        return self.session.follow_pagination(url=url, model=MonitoringMember, item_key='members', params=params)
