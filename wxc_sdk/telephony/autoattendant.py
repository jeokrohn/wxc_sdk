"""
Auto attendant data types and API
"""
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import Field

from wxc_sdk.common import AlternateNumber
from .forwarding import ForwardingApi, FeatureSelector
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..common import Greeting
from ..rest import RestSession

__all__ = ['Dialing', 'MenuKey', 'AutoAttendantAction', 'AutoAttendantKeyConfiguration', 'AutoAttendantMenu',
           'AutoAttendant', 'AutoAttendantApi']


class Dialing(str, Enum):
    """
    Dialing setting.
    """
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


class MenuKey(str, Enum):
    zero = '0'
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    six = '6'
    seven = '7'
    eight = '8'
    nine = '9'
    star = '*'
    pound = '#'


class AutoAttendantAction(str, Enum):
    """
    Auto Attendant Action
    """
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    name_dialing = 'NAME_DIALING'
    extension_dialing = 'EXTENSION_DIALING'
    repeat_menu = 'REPEAT_MENU'
    exit = 'EXIT'
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    return_to_previous_menu = 'RETURN_TO_PREVIOUS_MENU'
    play_announcement = 'PLAY_ANNOUNCEMENT'


class AutoAttendantKeyConfiguration(ApiModel):
    """
    Key configuration defined for the auto attendant.
    """
    #: Key assigned to specific menu configuration.
    key: MenuKey
    #: Action assigned to specific menu key configuration.
    action: AutoAttendantAction
    #: The description of each menu key.
    description: Optional[str]
    #: Value based on actions.
    value: Optional[str]

    @staticmethod
    def zero_exit() -> 'AutoAttendantKeyConfiguration':
        """
        0 -> EXIT

        :return: :class:`AutoAttendantKeyConfiguration`
        """
        return AutoAttendantKeyConfiguration(key=MenuKey.zero, action=AutoAttendantAction.exit)


class AutoAttendantMenu(ApiModel):
    """
    Menu defined for Auto Attendant
    """
    #: Greeting type defined for the auto attendant.
    greeting: Greeting
    #: Flag to indicate if auto attendant extension is enabled or not.
    extension_enabled: bool
    #: Key configurations defined for the auto attendant.
    key_configurations: list[AutoAttendantKeyConfiguration]

    @staticmethod
    def default() -> 'AutoAttendantMenu':
        """
        A default AA menu with a single key: 0 -> EXIT

        :return: :class:`AutoAttendantMenu`
        """
        return AutoAttendantMenu(greeting=Greeting.default,
                                 extension_enabled=True,
                                 key_configurations=[AutoAttendantKeyConfiguration.zero_exit()])


class AutoAttendant(ApiModel):
    """
    Auto attendant details
    """
    #: A unique identifier for the auto attendant.
    auto_attendant_id: Optional[str] = Field(alias='id')
    #: Unique name for the auto attendant.
    name: Optional[str]
    #: Name of location for auto attendant. (only returned by list())
    location_name: Optional[str]
    #: ID of location for auto attendant. (only returned by list())
    location_id: Optional[str]
    #: Flag to indicate if auto attendant number is enabled or not (only returned by details())
    enabled: Optional[bool]
    #: Auto attendant phone number. Either phone number or extension should be present as mandatory.
    phone_number: Optional[str]
    #: Auto attendant extension. Either phone number or extension should be present as mandatory.
    extension: Optional[str]
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]
    #: First name defined for an auto attendant. (only returned by details())
    first_name: Optional[str]
    #: Last name defined for an auto attendant. (only returned by details())
    last_name: Optional[str]
    #: Alternate numbers defined for the auto attendant. (only returned by details())
    alternate_numbers: Optional[list[AlternateNumber]]
    #: Language for the auto attendant.
    language: Optional[str]
    #: Language code for the auto attendant.
    language_code: Optional[str]
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str]
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str]
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[Dialing]
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[Dialing]
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str]
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[AutoAttendantMenu]
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[AutoAttendantMenu]

    def create_or_update(self) -> str:
        """
        Get JSON for create or update call

        :return: JSON
        :rtype: str
        """
        return self.json(exclude={'auto_attendant_id': True,
                                  'location_name': True,
                                  'location_id': True,
                                  'enabled': True,
                                  'toll_free_number': True,
                                  'language': True,
                                  })

    @staticmethod
    def create(*, name: str, business_schedule: str, phone_number: str = None,
               extension: str = None) -> 'AutoAttendant':
        """
        Get minimal auto attendant settings that can be used to create a new auto attendant by
        calling :meth:`AutoAttendantAPI.create` with these settings:

        .. code-block::

            ata = api.telephony.auto_attendant
            aa_settings = AutoAttendant.create(name=new_name,
                                               business_schedule=target_schedule.name,
                                               extension=extension)
            aa_id = ata.create(location_id=target_location.location_id,
                               settings=aa_settings)

        :param name: Unique name for the auto attendant.
        :type name: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param phone_number: Auto attendant phone number. Either phone number or extension should be present as
            mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension. Either phone number or extension should be present as mandatory.
        :type extension: str
        :return: :class:`AutoAttendant` instance
        """
        if not any((phone_number, extension)):
            raise ValueError('phone_number or extension have to be set')
        return AutoAttendant(name=name,
                             phone_number=phone_number,
                             extension=extension,
                             business_schedule=business_schedule,
                             business_hours_menu=AutoAttendantMenu.default(),
                             after_hours_menu=AutoAttendantMenu.default())


@dataclass(init=False)
class AutoAttendantApi(ApiChild, base='telephony/config/autoAttendants'):
    """
    Auto attendant API
    """
    forwarding: ForwardingApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.forwarding = ForwardingApi(session=session, feature_selector=FeatureSelector.auto_attendants)

    def _endpoint(self, *, location_id: str = None, auto_attendant_id: str = None) -> str:
        """
        auto attendant specific feature endpoint like /v1/telephony/config/locations/{locationId}/autoAttendants/{
        auto_attendant_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param auto_attendant_id: auto attendant id
        :type auto_attendant_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/autoAttendants')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/autoAttendants')
            if auto_attendant_id:
                ep = f'{ep}/{auto_attendant_id}'
            return ep

    def list(self, *, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> Generator[AutoAttendant, None, None]:
        """
        Read the List of Auto Attendants
        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :return: yields :class:`AutoAttendant` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AutoAttendant, params=params, item_key='autoAttendants')

    def by_name(self, *, name: str, location_id: str = None, org_id: str = None) -> Optional[AutoAttendant]:
        """
        Get auto attendant info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    def details(self, *, location_id: str, auto_attendant_id: str, org_id: str = None) -> AutoAttendant:
        """
        Get Details for an Auto Attendant
        Retrieve an Auto Attendant details.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str
        :return: auto attendant details
        :rtype: :class:`AutoAttendant`
        """
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        return AutoAttendant.parse_obj(self.get(url, params=params))

    def create(self, *, location_id: str, settings: AutoAttendant, org_id: str = None) -> str:
        """
        Create an Auto Attendant
        Create new Auto Attendant for the given location.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Creating an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param settings: auto attendant settings for new auto attendant
        :type settings: :class:`AutoAttendant`
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :return: ID of the newly created auto attendant.
        :rtype: str
        """
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = self.post(url, data=data, params=params)
        return data['id']

    def update(self, *, location_id: str, auto_attendant_id: str, settings: AutoAttendant, org_id: str = None):
        """
        Update an Auto Attendant
        Update the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Updating an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param settings: auto attendant settings for the update
        :type settings: :class:`AutoAttendant`
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        """
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        self.put(url, data=data, params=params)

    def delete_auto_attendant(self, *, location_id: str, auto_attendant_id: str, org_id: str = None):
        """
        elete the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Deleting an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete an auto attendant.
        :type location_id: str
        :param auto_attendant_id: Delete the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Delete the auto attendant from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url, params=params)
