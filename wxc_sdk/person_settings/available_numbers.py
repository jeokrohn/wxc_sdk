from collections.abc import Generator
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import NumberState, OwnerType, NumberOwner
from wxc_sdk.person_settings.common import ApiSelector
from wxc_sdk.rest import RestSession

__all__ = ['AvailableNumber', 'AvailablePhoneNumberLicenseType', 'AvailableNumbersApi']



class AvailableNumber(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 1235
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[NumberState] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates if the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[str] = None
    #: Mobile Network for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    #: example: mobileNetwork
    mobile_network: Optional[str] = None
    #: Routing Profile for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    #: example: AttRtPf
    routing_profile: Optional[str] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[NumberOwner] = None


class AvailablePhoneNumberLicenseType(str, Enum):
    var_standard = 'VAR_STANDARD'
    var_basic = 'VAR_BASIC'


class AvailableNumbersApi(ApiChild, base='telephony/config'):
    """
    API for person's available numbers

    Also used for virtual lines, workspaces

    Available methods

        ========================================== ============= ==========  ====
        Method                                     Virtual Lines Workspaces  User
        ========================================== ============= ==========  ====
        GET Call Forward Available Phone Numbers        X             X        X
        GET ECBN Available Phone Numbers                X             X        X
        GET Fax Message Available Phone Numbers         X                      X
        GET Available Phone Numbers                     X             X
        Get Call Intercept Available Phone Numbers                    X        X
        GET Primary Available Phone Numbers                                    X    
        GET Secondary Available Phone Numbers                                  X
        ========================================== ============= ==========  ====

    """

    # lookup for allowed entities for each function
    existing = {'callForwarding': {'virtualLines', 'workspaces', 'people'},
                'emergencyCallbackNumber': {'virtualLines', 'workspaces', 'people'},
                'faxMessage': {'virtualLines', 'people'},
                '': {'virtualLines', 'workspaces'},
                'callIntercept': {'workspaces', 'people'},
                'primary': {'people'},
                'secondary': {'people'}}

    def __init__(self, *, session: RestSession, selector: ApiSelector = ApiSelector.person):
        super().__init__(session=session)
        if selector == ApiSelector.person:
            self.selector = 'people'
        elif selector == ApiSelector.virtual_line:
            self.selector = 'virtualLines'
        elif selector == ApiSelector.workspace:
            self.selector = 'workspaces'

    def f_ep(self, available_for: str = None, entity_id: str = None) -> str:
        """
        Get endpoint URL
        
        :meta private:
        :param available_for: selector, something like callForwarding, faxMessage, ... 
        :param entity_id: entity id if needed
        :return: url
        """
        # does this feature exist
        allowed = self.existing.get(available_for)
        if allowed is None:
            raise ValueError(f'Invalid feature: {available_for}')
        if self.selector not in allowed:
            raise ValueError(f'endpoint {available_for} does not exist for {self.selector}')
        entity_id = entity_id and f'{entity_id}/' or ''
        available_for = available_for and f'{available_for}/' or ''
        url = self.ep(f'{self.selector}/{entity_id}{available_for}availableNumbers')
        return url

    def primary(self, location_id: str = None, phone_number: list[str] = None,
                license_type: AvailablePhoneNumberLicenseType = None,
                org_id: str = None,
                **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Person Primary Available Phone Numbers

        List numbers that are available to be assigned as a person's primary phone number.
        By default, this API returns standard and mobile numbers from all locations that are unassigned. The parameters
        `licenseType` and `locationId` must align with the person's settings to determine the appropriate number for
        assignment.
        Failure to provide these parameters may result in the unsuccessful assignment of the returned number.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope 
        of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param license_type: This is used to search numbers according to the person's `licenseType` to which the number
            will be assigned. Possible input values
        :type license_type: AvailablePhoneNumberLicenseType
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if license_type is not None:
            params['licenseType'] = enum_str(license_type)
        url = self.f_ep('primary')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def secondary(self, entity_id: str, phone_number: list[str] = None,
                  org_id: str = None,
                  **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Person Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a person's secondary phone number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
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
        url = self.f_ep('secondary', entity_id=entity_id)
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def fax_message(self, entity_id: str, phone_number: list[str] = None,
                    org_id: str = None,
                    **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Fax Message Available Phone Numbers

        Available for: user, virtual line

        List standard numbers that are available to be assigned as a FAX message number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope 
        of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.f_ep('faxMessage', entity_id=entity_id)
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def call_forward(self, entity_id: str, phone_number: list[str] = None,
                     owner_name: str = None, extension: str = None,
                     org_id: str = None,
                     **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Call Forward Available Phone Numbers

        Available for: user, virtual line, workspace

        List service and standard numbers that are available to be assigned as call forward number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope 
        of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
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
        url = self.f_ep('callForwarding', entity_id=entity_id)
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def ecbn(self, entity_id: str, phone_number: list[str] = None,
             owner_name: str = None, org_id: str = None,
             **params) -> Generator[AvailableNumber, None, None]:
        """
        Get ECBN Available Phone Numbers

        Available for: user, virtual line, workspace

        List standard numbers that are available to be assigned as emergency callback number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person.
        :type entity_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
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
        url = self.f_ep('emergencyCallbackNumber', entity_id=entity_id)
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def available(self, location_id: str = None, phone_number: list[str] = None,
                  org_id: str = None,
                  **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Available Phone Numbers

        Available for: virtual line, workspace

        List standard numbers that are available to be assigned as phone number.
        By default, this API returns numbers from all locations that are unassigned. To select the suitable number for
        assignment, ensure the entities location ID is provided as the `locationId` request parameter.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

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
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.f_ep('')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def call_intercept(self, entity_id: str, phone_number: list[str] = None,
                       owner_name: str = None, extension: str = None,
                       org_id: str = None,
                       **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Call Intercept Available Phone Numbers

        Available for: user, workspace

        List service and standard numbers that are available to be assigned as call intercept number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope 
        of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person.
        :type entity_id: str
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
        url = self.f_ep('callIntercept', entity_id=entity_id)
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)
