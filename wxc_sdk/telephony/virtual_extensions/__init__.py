from collections.abc import Generator
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['VirtualExtensionsApi', 'VirtualExtension', 'VirtualExtensionMode',
           'VirtualExtensionLevel', 'VirtualExtensionRange', 'VirtualExtensionRangeAction',
           'ValidateVirtualExtensionStatus', 'VirtualExtensionValidationStatus',
           'VirtualExtensionRangeValidationResult', 'ValidateVirtualExtensionRange',
           'PhoneNumberStatus', 'ValidatePhoneNumber']


class VirtualExtensionLevel(str, Enum):
    location = 'LOCATION'
    organization = 'ORGANIZATION'


class VirtualExtension(ApiModel):
    #: ID of the virtual extension.
    id: Optional[str] = None
    #: Extension of the virtual extension.
    extension: Optional[str] = None
    #: Routing prefix of the virtual extension's location.
    routing_prefix: Optional[str] = None
    #: ESN of the virtual extension.
    esn: Optional[str] = None
    #: Directory number of the virtual extension.
    phone_number: Optional[str] = None
    #: First name of the person at the virtual extension.
    first_name: Optional[str] = None
    #: Last name of the person at the virtual extension.
    last_name: Optional[str] = None
    #: Level of the virtual extension. It can be either `ORGANIZATION` or `LOCATION`.
    level: Optional[VirtualExtensionLevel] = None
    #: ID of the location to which the virtual extension is assigned. The location ID is a unique identifier for the
    #: location in Webex Calling.
    location_id: Optional[str] = None
    #: Name of the location to which the virtual extension is assigned.
    location_name: Optional[str] = None
    #: Display name of the person at the virtual extension.
    display_name: Optional[str] = None


class VirtualExtensionMode(str, Enum):
    standard = 'STANDARD'
    enhanced = 'ENHANCED'


class VirtualExtensionRange(ApiModel):
    #: ID of the virtual extension range.
    id: Optional[str] = None
    #: Name of the virtual extension range. This is a unique name for the virtual extension range.
    name: Optional[str] = None
    #: Prefix used for a virtual extension range. Prefix works in Standard and Enhanced modes. In Standard mode, it
    #: must be E.164 and it must be unique. In Enhanced mode, it can be E.164 or non-E.164.
    prefix: Optional[str] = None
    #: Level of the virtual extension range. It can be either `ORGANIZATION` or `LOCATION`.
    level: Optional[VirtualExtensionLevel] = None
    #: List of virtual extension patterns. The maximum number of patterns supported at a time is 100. Extension
    #: patterns can include one or more right-justified wildcards “X” matching any digit.
    patterns: Optional[list[str]] = None
    #: ID of the location to which the virtual extension range is assigned. This is set only for virtual extension
    #: ranges at the location level.
    location_id: Optional[str] = None
    #: Name of the location to which the virtual extension range is assigned. This is set only for virtual extension
    #: ranges at the location level
    location_name: Optional[str] = None


class VirtualExtensionRangeAction(str, Enum):
    #: Add new patterns to the existing virtual extension range.
    add = 'ADD'
    #: Remove existing patterns from the virtual extension range.
    remove = 'REMOVE'
    #: Replace existing patterns with new patterns in the virtual extension range.
    replace = 'REPLACE'


class ValidateVirtualExtensionStatus(str, Enum):
    #: Validation is successful.
    ok = 'OK'
    #: Validation failed.
    errors = 'ERRORS'


class VirtualExtensionValidationStatus(str, Enum):
    #: Validation is successful.
    valid = 'VALID'
    #: Duplicate patterns for virtual extension range.
    duplicate = 'DUPLICATE'
    #: Duplicate routing number in the pattern list.
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    #: Invalid prefix length.
    invalid = 'INVALID'
    #: Exceeding pattern limit of 100 in the request.
    limit_exceeded = 'LIMIT_EXCEEDED'


class VirtualExtensionRangeValidationResult(ApiModel):
    #: Name used for virtual extension range validation.
    name: Optional[str] = None
    #: Prefix used for a virtual extension range validation.
    prefix: Optional[str] = None
    #: Pattern used for a virtual extension range validation.
    pattern: Optional[str] = None
    #: Error code for the virtual extension range validation.
    error_code: Optional[int] = None
    #: Error message for the virtual extension range validation.
    message: Optional[str] = None
    #: Virtual extension range validation status.
    status: Optional[VirtualExtensionValidationStatus] = None


class ValidateVirtualExtensionRange(ApiModel):
    #: Virtual extension range validation status.
    status: Optional[ValidateVirtualExtensionStatus] = None
    #: Array of virtual extension range validation status. This is set only when the `status` is `ERRORS`.
    validation_status: Optional[list[VirtualExtensionRangeValidationResult]] = (
        Field(alias='virtualExtensionRangeValidationStatus', default=None))


class PhoneNumberStatus(ApiModel):
    phone_number: Optional[str] = None
    state: Optional[VirtualExtensionValidationStatus] = None
    error_code: Optional[int] = None
    message: Optional[str] = None


class ValidatePhoneNumber(ApiModel):
    status: Optional[ValidateVirtualExtensionStatus] = None
    phone_number_status: Optional[list[PhoneNumberStatus]] = Field(default_factory=list)


class VirtualExtensionsApi(ApiChild, base='telephony/config'):
    """
    Features: Virtual Extensions

    Features: Virtual Extensions allow assigning extensions to frequently called external numbers for simplified
    dialing within Webex Calling.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list_range(self, order: str = None, name: str = None, prefix: str = None,
                   location_id: str = None, org_level_only: bool = None,
                   org_id: str = None,
                   **params) -> Generator[VirtualExtensionRange, None, None]:
        """
        Get a list of a Virtual Extension Range

        Retrieves the list of Virtual Extension Ranges.

        Virtual extension ranges integrate remote workers on a separate telephony system into Webex Calling and enable
        extension dialing. Using these ranges, you can define patterns that can be used to route calls at a location
        level or an organization level. You are allowed to define virtual extensions ranges in addition to individual
        virtual extensions.
        This works in both Standard and Enhanced modes

        Retrieving a virtual extension range requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param order: Sort the list of virtual extension ranges by name or prefix, either ASC or DSC. Default sort
            order is ASC.
        :type order: str
        :param name: Filter the list of virtual extension ranges by name.
        :type name: str
        :param prefix: Filter the list of virtual extension ranges by prefix.
        :type prefix: str
        :param location_id: Filter the list of virtual extension ranges by location ID. Only one of the `locationId`
            and `OrgLevelOnly` query parameters is allowed at the same time.
        :type location_id: str
        :param org_level_only: Filter the list of virtual extension ranges by organization level. If `orgLevelOnly` is
            true, return only the organization level virtual extension ranges.
        :type org_level_only: bool
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :return: Generator yielding :class:`GetVirtualExtensionRangeListObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        if prefix is not None:
            params['prefix'] = prefix
        if location_id is not None:
            params['locationId'] = location_id
        if org_level_only is not None:
            params['orgLevelOnly'] = str(org_level_only).lower()
        url = self.ep('virtualExtensionRanges')
        return self.session.follow_pagination(url=url, model=VirtualExtensionRange,
                                              item_key='virtualExtensionRanges', params=params)

    def create_range(self, name: str, prefix: str, patterns: list[str] = None,
                     location_id: str = None, org_id: str = None) -> str:
        """
        Create a Virtual Extension Range

        Create a new Virtual Extension Range for the given organization or location.

        Virtual extension ranges integrate remote workers on a separate telephony system into Webex Calling and enable
        extension dialing. Using these ranges, you can define patterns that can be used to route calls at a location
        level or an organization level. You are allowed to define virtual extensions ranges in addition to individual
        virtual extensions.
        This works in both Standard and Enhanced modes

        Virtual extension range can be set up at the organization or location level.

        Creating a virtual extension range requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param name: Name of the virtual extension range. This is a unique name for the virtual extension range.
        :type name: str
        :param prefix: Prefix used for a virtual extension range. Prefix works in Standard and Enhanced modes. In
            Standard mode, it must be E.164 and unique. In Enhanced mode, it can be E.164 or non-E.164.
        :type prefix: str
        :param patterns: List of virtual extension patterns. You can add up to 100 patterns at a time. Extension
            patterns can include one or more right-justified wildcards “X” matching any digit.
        :type patterns: list[str]
        :param location_id: ID of the location to which the virtual extension range is assigned. The location ID is a
            unique identifier for the location in Webex Calling. This is set only when location level virtual
            extension range is added.
        :type location_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['prefix'] = prefix
        if patterns is not None:
            body['patterns'] = patterns
        if location_id is not None:
            body['locationId'] = location_id
        url = self.ep('virtualExtensionRanges')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def validate_range(self, location_id: str = None,
                       name: str = None, prefix: str = None,
                       patterns: list[str] = None,
                       range_id: str = None,
                       org_id: str = None) -> ValidateVirtualExtensionRange:
        """
        Validate the prefix and extension pattern for a Virtual Extension Range.

        Virtual extension ranges integrate remote workers on a separate telephony system into Webex Calling and enable
        extension dialing. Using these ranges, you can define patterns that can be used to route calls at a location
        level or an organization level. You are allowed to define virtual extensions ranges in addition to individual
        virtual extensions.
        This works in both Standard and Enhanced modes

        Validating a prefix and extension pattern for a Virtual Extension Range requires a full administrator or
        location administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: ID of the location to which the virtual extension range is assigned. The location ID is a
            unique identifier for the location in Webex Calling.
        :type location_id: str
        :param name: Name of the virtual extension range. This is a unique name for the virtual extension range.
        :type name: str
        :param prefix: Prefix used for a virtual extension range.
        :type prefix: str
        :param patterns: List of virtual extension patterns. The maximum number of patterns supported at a time is 100.
        :type patterns: list[str]
        :param range_id: ID of the virtual extension range. This is mandatory when validating for an existing virtual
            extension range, not present when validating a new virtual extension range before adding it.
        :type range_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: :class:`ValidateVirtualExtensionRange`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if location_id is not None:
            body['locationId'] = location_id
        if name is not None:
            body['name'] = name
        if prefix is not None:
            body['prefix'] = prefix
        if patterns is not None:
            body['patterns'] = patterns
        if range_id is not None:
            body['rangeId'] = range_id
        url = self.ep('virtualExtensionRanges/actions/validate/invoke')
        data = super().post(url, params=params, json=body)
        r = ValidateVirtualExtensionRange.model_validate(data)
        return r

    def delete_range(self, extension_range_id: str, org_id: str = None):
        """
        Delete a Virtual Extension Range

        Delete a virtual extension range for the given extension range ID.

        Virtual extension ranges integrate remote workers on a separate telephony system into Webex Calling and enable
        extension dialing. Using these ranges, you can define patterns that can be used to route calls at a location
        level or an organization level. You are allowed to define virtual extensions ranges in addition to individual
        virtual extensions.
        This works in both Standard and Enhanced modes

        Deleting a virtual extension range requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param extension_range_id: ID of the virtual extension range.
        :type extension_range_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'virtualExtensionRanges/{extension_range_id}')
        super().delete(url, params=params)

    def details_range(self, extension_range_id: str,
                      org_id: str = None) -> VirtualExtensionRange:
        """
        Get details of a Virtual Extension Range

        Retrieve virtual extension range details for the given extension range ID.

        Virtual extension ranges integrate remote workers on a separate telephony system into Webex Calling and enable
        extension dialing. Using these ranges, you can define patterns that can be used to route calls at a location
        level or an organization level. You are allowed to define virtual extensions ranges in addition to individual
        virtual extensions.
        This works in both Standard and Enhanced modes

        Retrieving a virtual extension range requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param extension_range_id: ID of the virtual extension range.
        :type extension_range_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: :class:`VirtualExtensionRange`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'virtualExtensionRanges/{extension_range_id}')
        data = super().get(url, params=params)
        r = VirtualExtensionRange.model_validate(data)
        return r

    def modify_range(self, extension_range_id: str, name: str = None, prefix: str = None,
                     patterns: list[str] = None,
                     action: VirtualExtensionRangeAction = None, org_id: str = None):
        """
        Modify Virtual Extension Range

        Modify virtual extension range for the given extension range ID.

        Virtual extension ranges integrate remote workers on a separate telephony system into Webex Calling and enable
        extension dialing. Using these ranges, you can define patterns that can be used to route calls at a location
        level or an organization level. You are allowed to define virtual extensions ranges in addition to individual
        virtual extensions.
        This works in both Standard and Enhanced modes

        Modifying a virtual extension range requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param extension_range_id: ID of the virtual extension range.
        :type extension_range_id: str
        :param name: Name of the virtual extension range. This is a unique name for the virtual extension range.
        :type name: str
        :param prefix: Prefix used for a virtual extension range.
        :type prefix: str
        :param patterns: The pattern to be added, replaced, or removed from a virtual extension range. The maximum
            number of patterns supported at a time is 100.
        :type patterns: list[str]
        :param action: Action to be performed on the virtual extension range. It can be either `ADD`, `REMOVE` or
            `REPLACE`. This is mandatory when `patterns` are provided.
        :type action: VirtualExtensionRangeAction
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if prefix is not None:
            body['prefix'] = prefix
        if patterns is not None:
            body['patterns'] = patterns
        if action is not None:
            body['action'] = enum_str(action)
        url = self.ep(f'virtualExtensionRanges/{extension_range_id}')
        super().put(url, params=params, json=body)

    def list_extensions(self, order: str = None, extension: str = None, phone_number: str = None,
                        name: str = None, location_name: str = None, location_id: str = None,
                        org_level_only: bool = None, org_id: str = None,
                        **params) -> Generator[VirtualExtension, None, None]:
        """
        Read the List of Virtual Extensions

        Retrieve virtual extensions associated with a specific customer.

        The GET Virtual Extensions API allows administrators to retrieve a list of virtual extensions configured within
        their organization. Virtual extensions enable users to dial extension numbers that route to external phone
        numbers, such as those of remote workers or frequently contacted clients.
        This API returns key information including the  extension, associated  phone number (in E.164 format), display
        name, and the location to which the virtual extension belongs
        The API supports filtering by various parameters, such as extension number, phone number, and location name.
        The results can be paginated using the `max` and `start` parameters, and the order of the results can be
        specified using the `order` parameter.

        Retrieving a Virtual Extension requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param order: Order the list of virtual extensions in ascending or descending order. Default is ascending.
        :type order: str
        :param extension: Filter the list of virtual extensions by extension number.
        :type extension: str
        :param phone_number: Filter the list of virtual extensions by phone number.
        :type phone_number: str
        :param name: Filter the list of virtual extensions by name. This can be either first name or last name.
        :type name: str
        :param location_name: Filter the list of virtual extensions by location name.(Only one of the locationName,
            locationId, and OrgLevelOnly query parameters is allowed at the same time.)
        :type location_name: str
        :param location_id: Filter the list of virtual extensions by location ID.
        :type location_id: str
        :param org_level_only: Filter the list of virtual extensions by organization level. If orgLevelOnly is true,
            return only the organization level virtual extensions.
        :type org_level_only: bool
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :return: Generator yielding :class:`GetVirtualExtensionObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if extension is not None:
            params['extension'] = extension
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if name is not None:
            params['name'] = name
        if location_name is not None:
            params['locationName'] = location_name
        if location_id is not None:
            params['locationId'] = location_id
        if org_level_only is not None:
            params['orgLevelOnly'] = str(org_level_only).lower()
        url = self.ep('virtualExtensions')
        return self.session.follow_pagination(url=url, model=VirtualExtension, item_key='virtualExtensions',
                                              params=params)

    def create_extension(self, display_name: str, phone_number: str, extension: str, first_name: str = None,
                         last_name: str = None, location_id: str = None, org_id: str = None) -> str:
        """
        Create a Virtual Extension

        Create new Virtual Extension for the given organization or location.

        You can set up virtual extensions at the organization or location level. The organization level enables
        everyone across your organization to dial the same extension number to reach someone.
        You can use the location level virtual extension like any other extension assigned to the specific location.
        Users at the specific location can dial the extension. However, users at other locations can reach the virtual
        extension by dialing the ESN.

        Creating a virtual extension requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write` and `Identity:contact`.

        :param display_name: Display name of the person at the virtual extension.
        :type display_name: str
        :param phone_number: Directory number of the virtual extension.
        :type phone_number: str
        :param extension: Extension of the virtual extension.
        :type extension: str
        :param first_name: First name of the person at the virtual extension.
        :type first_name: str
        :param last_name: Last name of the person at the virtual extension.
        :type last_name: str
        :param location_id: ID of the location to which the virtual extension is assigned. The location ID is a unique
            identifier for the location in Webex Calling.
        :type location_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        body['displayName'] = display_name
        body['phoneNumber'] = phone_number
        body['extension'] = extension
        if location_id is not None:
            body['locationId'] = location_id
        url = self.ep('virtualExtensions')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def validate_external_phone_number(self, phone_numbers: list[str], org_id: str = None) -> ValidatePhoneNumber:
        """
        Validate an external phone number

        Validate external phone number for the given organization.

        This API is designed to validate external phone numbers before they are assigned as virtual extensions for a
        customer.
        It ensures that the provided numbers are properly formatted, eligible for use, and not already in use within
        the system.
        This validation is typically part of a pre-check process during provisioning or number assignment workflows,
        helping administrators or systems prevent conflicts or errors related to number reuse or format issues.

        Creating a virtual extension requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param phone_numbers: List of external phone numbers to be validated.
        :type phone_numbers: list[str]
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: ValidatePhoneNumber
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['phoneNumbers'] = phone_numbers
        url = self.ep('virtualExtensions/actions/validateNumbers/invoke')
        data = super().post(url, params=params, json=body)
        r = ValidatePhoneNumber.model_validate(data)
        return r

    def get_extension_settings(self, org_id: str = None) -> VirtualExtensionMode:
        """
        Get Virtual extension settings

        Retrieve Virtual Extension settings for the given Org.

        This API retrieves the virtual extension mode settings configured for a given organization. Virtual extensions
        can operate in two modes: STANDARD and ENHANCED. The selected mode determines how the system handles routing
        and signaling for virtual extensions.
        By default, the virtual extensions that you create use the Standard mode. Another mode, enhanced signaling
        mode, is available to all customers, however, virtual extensions won't function properly in this mode unless
        your PSTN provider supports special network signaling extensions and there aren't many PSTN providers that do.

        Retrieving a Virtual Extension settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: VirtualExtensionMode
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('virtualExtensions/settings')
        data = super().get(url, params=params)
        r = VirtualExtensionMode.model_validate(data['mode'])
        return r

    def modify_extension_settings(self, mode: VirtualExtensionMode, org_id: str = None):
        """
        Modify Virtual Extension Settings

        Update Virtual Extension details for the given extension ID.

        This endpoint updates the virtual extension settings for an organization. It is primarily used to configure the
        operating mode for virtual extensions.
        Modes determine how virtual extensions are assigned or managed within the system.

        Updating a Virtual Extension requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode: Mode of the virtual extension. It can be either `STANDARD` or `ENHANCED`.

        + `STANDARD` -  Standard Virtual extension mode in which virtual extensions must be associated with a valid
        E.164 number, but this requires no enhanced signaling support from the PSTN provider.
        + `ENHANCED` - Enhanced signaling mode: only a few PSTN providers support this special network signaling
        extension.
        :type mode: VirtualExtensionMode
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['mode'] = enum_str(mode)
        url = self.ep('virtualExtensions/settings')
        super().put(url, params=params, json=body)

    def delete_extension(self, extension_id: str, org_id: str = None):
        """
        Delete a Virtual Extension

        Delete Virtual Extension using the extension ID.

        This API permanently deletes a virtual extension from the organization. Once deleted, the extension will no
        longer route calls to the external phone number, and users won’t be able to reach it via the assigned
        extension.

        Deleting a Virtual Extension requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write` and `Identity:contact`.

        :param extension_id: ID of the virtual extension.
        :type extension_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'virtualExtensions/{extension_id}')
        super().delete(url, params=params)

    def details_extension(self, extension_id: str, org_id: str = None) -> VirtualExtension:
        """
        Get a Virtual Extension

        Retrieve Virtual Extension details for the given extension ID.

        Virtual extensions integrate remote workers on separate telephony systems into Webex Calling, enabling users to
        reach them via extension dialing.
        This endpoint allows administrators to retrieve configuration details for a specific virtual extension,
        ensuring visibility into the mapping between extensions and external phone numbers.

        Retrieving a Virtual Extension requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param extension_id: ID of the virtual extension.
        :type extension_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: :class:`VirtualExtension`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'virtualExtensions/{extension_id}')
        data = super().get(url, params=params)
        r = VirtualExtension.model_validate(data)
        return r

    def update_extension(self, extension_id: str, first_name: str = None, last_name: str = None,
                         display_name: str = None, phone_number: str = None, extension: str = None,
                         org_id: str = None):
        """
        Update a Virtual Extension

        Update Virtual Extension details for the given extension ID.

        This API updates the configuration of an existing virtual extension identified by its unique extension ID.
        Administrators can modify fields such as the extension, associated phone number (in E.164 format), display
        name, and location etc.

        Updating a Virtual Extension requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write` and `Identity:contact`.

        :param extension_id: ID of the virtual extension.
        :type extension_id: str
        :param first_name: First name of the person at the virtual extension.
        :type first_name: str
        :param last_name: Last name of the person at the virtual extension.
        :type last_name: str
        :param display_name: Display name of the person at the virtual extension.
        :type display_name: str
        :param phone_number: Directory number of the virtual extension.
        :type phone_number: str
        :param extension: Extension of the virtual extension.
        :type extension: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if display_name is not None:
            body['displayName'] = display_name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'virtualExtensions/{extension_id}')
        super().put(url, params=params, json=body)
