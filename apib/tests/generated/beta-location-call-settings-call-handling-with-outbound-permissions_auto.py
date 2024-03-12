from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaLocationCallSettingsCallHandlingWithOutboundPermissionsApi', 'LocationDigitPatternObject',
           'LocationOutgoingPermissionDigitPatternPostObjectAction']


class LocationOutgoingPermissionDigitPatternPostObjectAction(str, Enum):
    #: Allow the designated call type.
    allow = 'ALLOW'
    #: Block the designated call type.
    block = 'BLOCK'
    #: Allow only via Authorization Code.
    auth_code = 'AUTH_CODE'
    #: Transfer to Auto Transfer Number 1. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Transfer to Auto Transfer Number 2. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Transfer to Auto Transfer Number 3. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class LocationDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFL1FWVlVUMEZVVkVWT1JFRk9WQzFDVlZOSlRrVlRVeTFJVDFWU1V3
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    #: example: DigitPattern1
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    #: example: 1XXX
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches with the digit pattern.
    #: example: ALLOW
    action: Optional[LocationOutgoingPermissionDigitPatternPostObjectAction] = None
    #: Option to allow or disallow transfer of calls.
    #: example: True
    transfer_enabled: Optional[bool] = None


class BetaLocationCallSettingsCallHandlingWithOutboundPermissionsApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Location Call Settings: Call Handling with Outbound Permissions
    
    Manage the outgoing calling permissions for a location.
    
    Viewing these outgoing calling permission settings requires a full or read-only or location administrator auth
    token with a scope of `spark-admin:telephony_config_read`.
    
    Modifying these outgoing calling permission settings requires a full administrator or location administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def delete_outgoing_permission_location_access_code(self, location_id: str, org_id: str = None):
        """
        Delete Outgoing Permission Location Access Code

        Deletes all the access codes for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Deleting the access codes requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param location_id: Deletes all the access codes for this location.
        :type location_id: str
        :param org_id: Deletes the access codes for a customer location.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def get_outgoing_permission_digit_pattern(self, location_id: str,
                                              org_id: str = None) -> list[LocationDigitPatternObject]:
        """
        Get Outgoing Permission Digit Pattern

        Get the digit patterns for the outbound permission in a location.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Retrieving digit patterns requires a full or read-only administrator or location administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve digit patterns for this location.
        :type location_id: str
        :param org_id: Retrieve digit patterns from this organization.
        :type org_id: str
        :rtype: list[LocationDigitPatternObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = TypeAdapter(list[LocationDigitPatternObject]).validate_python(data['digitPatterns'])
        return r

    def get_details_for_a_outgoing_permission_digit_pattern(self, location_id: str, digit_pattern_id: str,
                                                            org_id: str = None) -> LocationDigitPatternObject:
        """
        Get Details for a Outgoing Permission Digit Pattern

        Get the digit pattern details.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Retrieving digit pattern details requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve digit pattern details for this location.
        :type location_id: str
        :param digit_pattern_id: Retrieve the digit pattern with the matching ID.
        :type digit_pattern_id: str
        :param org_id: Retrieve digit pattern details from this organization.
        :type org_id: str
        :rtype: :class:`LocationDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = LocationDigitPatternObject.model_validate(data)
        return r

    def create_outgoing_permission_a_new_digit_pattern_for_a_customer_location(self, location_id: str, name: str,
                                                                               pattern: str,
                                                                               action: LocationOutgoingPermissionDigitPatternPostObjectAction,
                                                                               transfer_enabled: bool,
                                                                               org_id: str = None) -> str:
        """
        Create Outgoing Permission a new Digit Pattern for a customer location

        Add a new digit pattern for the given location for a customer.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Creating a digit pattern requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Add new digit pattern for this location.
        :type location_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches with the digit pattern.
        :type action: LocationOutgoingPermissionDigitPatternPostObjectAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: Add new digit pattern for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['pattern'] = pattern
        body['action'] = enum_str(action)
        body['transferEnabled'] = transfer_enabled
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def update_a_outgoing_permission_digit_pattern(self, location_id: str, digit_pattern_id: str, name: str = None,
                                                   pattern: str = None,
                                                   action: LocationOutgoingPermissionDigitPatternPostObjectAction = None,
                                                   transfer_enabled: bool = None, org_id: str = None):
        """
        Update a Outgoing Permission Digit Pattern

        Update the designated digit pattern.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Updating a digit pattern requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update digit pattern for this location.
        :type location_id: str
        :param digit_pattern_id: Update digit pattern with the matching ID.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches with the digit pattern.
        :type action: LocationOutgoingPermissionDigitPatternPostObjectAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: Update digit pattern for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if pattern is not None:
            body['pattern'] = pattern
        if action is not None:
            body['action'] = enum_str(action)
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def delete_a_outgoing_permission_digit_pattern(self, location_id: str, digit_pattern_id: str, org_id: str = None):
        """
        Delete a Outgoing Permission Digit Pattern

        Delete the designated digit pattern.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Deleting a digit pattern requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Delete digit pattern for this location.
        :type location_id: str
        :param digit_pattern_id: Delete digit pattern with the matching ID.
        :type digit_pattern_id: str
        :param org_id: Delete digit pattern for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def delete_all_outgoing_permission_digit_patterns(self, location_id: str, org_id: str = None):
        """
        Delete all Outgoing Permission Digit Patterns

        Deletes all the digit patterns for a particular location for a customer.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Deleting the digit patterns requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Delete digit patterns for this location.
        :type location_id: str
        :param org_id: Delete digit patterns for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)
