"""
Auto attendant data types and API
"""
from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional, List

from pydantic import Field, TypeAdapter

from .forwarding import ForwardingApi, FeatureSelector
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..base import SafeEnum as Enum
from ..common import Greeting, AlternateNumber, MediaFileType, AnnAudioFile
from ..person_settings.available_numbers import AvailableNumber
from ..rest import RestSession

__all__ = ['Dialing', 'MenuKey', 'AutoAttendantAction', 'AutoAttendantKeyConfiguration',
           'AutoAttendantMenu', 'AutoAttendant', 'AutoAttendantApi', 'CallTreatmentRetry', 'ActionToBePerformed',
           'ActionToBePerformedAction', 'CallTreatment']


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
    description: Optional[str] = None
    #: Value based on actions.
    value: Optional[str] = None

    @staticmethod
    def zero_exit() -> 'AutoAttendantKeyConfiguration':
        """
        0 -> EXIT

        :return: :class:`AutoAttendantKeyConfiguration`
        """
        return AutoAttendantKeyConfiguration(key=MenuKey.zero, action=AutoAttendantAction.exit)


class AutoAttendantAudioFile(ApiModel):
    name: str
    media_type: MediaFileType


class CallTreatmentRetry(str, Enum):
    #: Announcement will not be repeated.
    no_repeat = 'NO_REPEAT'
    #: Repeat the announcement once.
    one_time = 'ONE_TIME'
    #: Repeat the announcement twice.
    two_times = 'TWO_TIMES'
    #: Repeat the announcement thrice.
    three_times = 'THREE_TIMES'


class ActionToBePerformedAction(str, Enum):
    #: Plays a recorded message and then disconnects the call.
    play_message_and_disconnect = 'PLAY_MESSAGE_AND_DISCONNECT'
    #: Transfers the call to the specified number, without playing a transfer prompt.
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    #: Plays the message and then transfers the call to the specified number.
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    #: Plays the message and then transfers the call to the specified operator number.
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    #: Transfers the call to the configured mailbox, without playing a transfer prompt.
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    #: Disconnect the call.
    disconnect = 'DISCONNECT'


class ActionToBePerformed(ApiModel):
    #: Action to perform after the retry attempt is reached.
    action: Optional[ActionToBePerformedAction] = None
    #: Greeting type is defined when `action` is set to `PLAY_MESSAGE_AND_DISCONNECT`.
    greeting: Optional[Greeting] = None
    #: Pre-configured announcement audio files when `action` is set to `PLAY_MESSAGE_AND_DISCONNECT` and `greeting` is
    #: set to `CUSTOM`.
    audio_announcement_file: Optional[AnnAudioFile] = None
    #: Transfer call to the specified number when `action` is set to `TRANSFER_WITH_PROMPT`, `TRANSFER_WITHOUT_PROMPT`
    #: and `TRANSFER_TO_OPERATOR` and `TRANSFER_TO_MAILBOX`.
    transfer_call_to: Optional[str] = None


class CallTreatment(ApiModel):
    #: Number of times to repeat the Welcome greeting when the user does not provide an input. By default, NO_REPEAT is
    #: set.
    retry_attempt_for_no_input: Optional[CallTreatmentRetry] = None
    #: Interval the Auto Attendant service waits before timing out. By default, 10 seconds. Min value is 1 and max
    #: value is 60.
    no_input_timer: Optional[int] = None
    #: Action to perform after the retry attempt is reached.
    action_to_be_performed: Optional[ActionToBePerformed] = None


class AutoAttendantMenu(ApiModel):
    """
    Menu defined for Auto Attendant
    """
    #: Greeting type defined for the auto attendant.
    greeting: Greeting
    #: Flag to indicate if auto attendant extension is enabled or not.
    extension_enabled: bool
    #: Announcement Audio File details.
    audio_announcement_file: Optional[AnnAudioFile] = None
    #: Key configurations defined for the auto attendant.
    key_configurations: list[AutoAttendantKeyConfiguration]
    #: Call treatment details.
    call_treatment: Optional[CallTreatment] = None

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
    auto_attendant_id: Optional[str] = Field(alias='id', default=None)
    #: Unique name for the auto attendant.
    name: Optional[str] = None
    #: Name of location for auto attendant. (only returned by list())
    location_name: Optional[str] = None
    #: ID of location for auto attendant. (only returned by list())
    location_id: Optional[str] = None
    #: Flag to indicate if auto attendant number is enabled or not (only returned by details())
    enabled: Optional[bool] = None
    #: Auto attendant phone number. Either phone number or extension should be present as mandatory.
    phone_number: Optional[str] = None
    #: Auto attendant extension. Either phone number or extension should be present as mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routingPrefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: First name defined for an auto attendant. (only returned by details())
    first_name: Optional[str] = None
    #: Last name defined for an auto attendant. (only returned by details())
    last_name: Optional[str] = None
    #: Alternate numbers defined for the auto attendant. (only returned by details())
    alternate_numbers: Optional[list[AlternateNumber]] = None
    #: Language for the auto attendant.
    language: Optional[str] = None
    #: Language code for the auto attendant.
    language_code: Optional[str] = None
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str] = None
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str] = None
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[Dialing] = None
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[Dialing] = None
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str] = None
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[AutoAttendantMenu] = None
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[AutoAttendantMenu] = None

    def create_or_update(self) -> str:
        """
        Get JSON for create or update call

        :return: JSON
        :rtype: str
        """
        return self.model_dump_json(exclude={'auto_attendant_id': True,
                                             'location_name': True,
                                             'location_id': True,
                                             'enabled': True,
                                             'toll_free_number': True,
                                             'language': True,
                                             'esn': True,
                                             'routing_prefix': True
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


@dataclass(init=False, repr=False)
class AutoAttendantApi(ApiChild, base='telephony/config/autoAttendants'):
    """
    Features:  Auto Attendant

    Features: Auto Attendant support reading and writing of Webex Calling Auto Attendant settings for a specific
    organization.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """
    forwarding: ForwardingApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.forwarding = ForwardingApi(session=session, feature_selector=FeatureSelector.auto_attendants)

    def _endpoint(self, *, location_id: str = None, auto_attendant_id: str = None, path: str = None) -> str:
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
            if path:
                ep = f'{ep}/{path}'
            return ep

    def list(self, org_id: str = None, location_id: str = None, name: str = None,
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

    def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[AutoAttendant]:
        """
        Get auto attendant info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    def details(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> AutoAttendant:
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
        return AutoAttendant.model_validate(self.get(url, params=params))

    def create(self, location_id: str, settings: AutoAttendant, org_id: str = None) -> str:
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

    def update(self, location_id: str, auto_attendant_id: str, settings: AutoAttendant, org_id: str = None):
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

    def delete_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None):
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

    def primary_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                        org_id: str = None,
                                        **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Auto Attendant Primary Available Phone Numbers

        List service and standard numbers that are available to be assigned as the auto attendant's primary phone
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self._endpoint(location_id=location_id, path='availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def alternate_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                          org_id: str = None,
                                          **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Auto Attendant Alternate Available Phone Numbers

        List service and standard numbers that are available to be assigned as the auto attendant's alternate number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self._endpoint(location_id=location_id, path='alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def call_forward_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                             owner_name: str = None, extension: str = None,
                                             org_id: str = None,
                                             **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Auto Attendant Call Forward Available Phone Numbers

        List service and standard numbers that are available to be assigned as the auto attendant's call forward
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self._endpoint(location_id=location_id, path='callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def list_announcement_files(self, location_id: str, auto_attendant_id: str,
                                org_id: str = None) -> List[AnnAudioFile]:
        """
        Read the List of Auto Attendant Announcement Files

        List file info for all auto attendant announcement files associated with this auto attendant.

        Auto attendant announcement files contain messages and music that callers hear while waiting in the queue. A
        auto attendant can be configured to play whatever subset of these announcement files is desired.

        Retrieving this list of files requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        Note that uploading of announcement files via API is not currently supported, but is available via Webex
        Control Hub.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve announcement files for the auto attendant with this identifier.
        :type auto_attendant_id: str
        :param org_id: Retrieve announcement files for an auto attendant from this organization.
        :type org_id: str
        :rtype: list[AnnAudioFile]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.session.ep(
            f'telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AnnAudioFile]).validate_python(data['announcements'])
        return r

    def delete_announcement_file(self, location_id: str, auto_attendant_id: str, file_name: str,
                                 org_id: str = None):
        """
        Delete an Auto Attendant Announcement File

        Delete an announcement file for the designated auto attendant.

        Auto Attendant announcement files contain messages and music that callers hear while waiting in the queue. A
        auto attendant can be configured to play whatever subset of these announcement files is desired.

        Deleting an announcement file for a auto attendant requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Delete an announcement for a auto attendant in this location.
        :type location_id: str
        :param auto_attendant_id: Delete an announcement for the auto attendant with this identifier.
        :type auto_attendant_id: str
        :type file_name: str
        :param org_id: Delete auto attendant announcement from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.session.ep(
            f'telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements/{file_name}')
        super().delete(url, params=params)
