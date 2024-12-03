from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesOperatingModeManagementForPersonCallSettingsApi', 'ExceptionTypeObject', 'Location',
           'ModeManagementFeatureTypeObject', 'UserModeManagementAvailableFeaturesObject',
           'UserModeManagementFeatureObject']


class ModeManagementFeatureTypeObject(str, Enum):
    #: Specifies the feature is an Auto Attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: Specifies the feature is a Call Queue.
    call_queue = 'CALL_QUEUE'
    #: Specifies the feature is a Hunt Group.
    hunt_group = 'HUNT_GROUP'


class UserModeManagementAvailableFeaturesObject(ApiModel):
    #: A unique identifier for the feature.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzA1NTJmNjdiLTU5YTktNDFiYi04NzM2LTFiMDQxZDFkZGQ1ZQ
    id: Optional[str] = None
    #: Unique name for the feature.
    #: example: Test Feature
    name: Optional[str] = None
    #: Defines the scheduling of the operating mode.
    #: example: AUTO_ATTENDANT
    type: Optional[ModeManagementFeatureTypeObject] = None
    #: The primary phone number configured for the feature.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: The extension configured for the feature.
    #: example: 28
    extension: Optional[str] = None


class ExceptionTypeObject(str, Enum):
    #: The mode was switched to or extended by the user for manual switch back and runs as an exception until the user
    #: manually switches the feature back to normal operation or a different mode.
    manual_switch_back = 'MANUAL_SWITCH_BACK'
    #: The mode was switched to by the user before its start time and runs as an exception until its end time is
    #: reached, at which point it automatically switches the feature back to normal operation.
    automatic_switch_back_early_start = 'AUTOMATIC_SWITCH_BACK_EARLY_START'
    #: The current mode was extended by the user before its end time and runs as an exception until the extension end
    #: time (mode's end time + extension of up to 12 hours) is reached, at which point it automatically switches the
    #: feature back to normal operation.
    automatic_switch_back_extension = 'AUTOMATIC_SWITCH_BACK_EXTENSION'
    #: The mode will remain the current operating mode for the feature until its normal end time is reached.
    automatic_switch_back_standard = 'AUTOMATIC_SWITCH_BACK_STANDARD'


class Location(ApiModel):
    #: Location identifier associated with the feature.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    id: Optional[str] = None
    #: Location name associated with the feature.
    #: example: Banglore
    name: Optional[str] = None


class UserModeManagementFeatureObject(ApiModel):
    #: A unique identifier for the feature.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzA1NTJmNjdiLTU5YTktNDFiYi04NzM2LTFiMDQxZDFkZGQ1ZQ
    id: Optional[str] = None
    #: Unique name for the feature.
    #: example: Test Feature
    name: Optional[str] = None
    #: Defines the scheduling of the operating mode.
    type: Optional[ModeManagementFeatureTypeObject] = None
    #: The primary phone number configured for the feature.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: The extension configured for the feature.
    #: example: 28
    extension: Optional[str] = None
    #: A flag to indicate whether mode-based call forwarding is enabled for the feature.
    #: example: True
    mode_based_forwarding_enabled: Optional[bool] = None
    #: The destination for call forwarding if mode-based call forwarding is enabled.
    #: example: +19705550028
    forward_destination: Optional[str] = None
    #: Name of the current operating mode.
    #: example: Day Operating Mode
    current_operating_mode_name: Optional[str] = None
    #: Unique identifier for the current operating mode.
    #: example: Y2lzY29zcGFyazovL3VzL09QRVJBVElOR19NT0RFLzIxM2I1ZTIwLTljMjAtNDUwNi1iYWE3LTE0OGE0NWQyZWY4OQ
    current_operating_mode_id: Optional[str] = None
    #: Defines the exception through which the current operating mode is set as active for the feature.
    #: example: MANUAL_SWITCH_BACK
    exception_type: Optional[ExceptionTypeObject] = None
    #: Location object that has a unique identifier for the location and its name.
    location: Optional[Location] = None


class BetaFeaturesOperatingModeManagementForPersonCallSettingsApi(ApiChild, base='telephony/config/people'):
    """
    Beta Features: Operating Mode Management for Person Call Settings
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator or location administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by
    a person to read their own settings.
    
    Configuring People settings requires a full, or user administrator or location administrator auth token with the
    `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope can be
    used by a person to update their own settings.
    
    Call Settings API access can be restricted via Control Hub by a full administrator. Restricting access causes the
    APIs to throw a `403 Access Forbidden` error.
    
    See details about `features available by license type for Webex Calling
    <https://help.webex.com/en-us/article/n1qbbp7/Features-available-by-license-type-for-Webex-Calling>`_.
    """

    def retrieve_the_list_of_available_features_(self, person_id: str = None, name: str = None,
                                                 phone_number: str = None, extension: str = None, order: str = None,
                                                 org_id: str = None,
                                                 **params) -> Generator[UserModeManagementAvailableFeaturesObject, None, None]:
        """
        Retrieve the List of Available Features.

        Retrieve a list of feature identifiers that can be assigned to a user for `Mode Management`. Feature
        identifiers reference feature instances like `Auto Attendants`, `Call Queues`, and `Hunt Groups`.

        Features with mode-based call forwarding enabled can be assigned to a user for `Mode Management`.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param name: List features whose `name` contains this string.
        :type name: str
        :param phone_number: List features whose phoneNumber contains this matching string.
        :type phone_number: str
        :param extension: List features whose `extension` contains this matching string.
        :type extension: str
        :param order: Sort the list of features based on `name`, `phoneNumber`, or `extension`, either `asc`, or
            `desc`.
        :type order: str
        :param org_id: Retrieve features list from this organization.
        :type org_id: str
        :return: Generator yielding :class:`UserModeManagementAvailableFeaturesObject` instances
        """
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        if order is not None:
            params['order'] = order
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/modeManagement/availableFeatures')
        return self.session.follow_pagination(url=url, model=UserModeManagementAvailableFeaturesObject, item_key='features', params=params)

    def retrieve_the_list_of_features_assigned_to_a_user_for_mode_management_(self, person_id: str = None,
                                                                              org_id: str = None) -> list[UserModeManagementFeatureObject]:
        """
        Retrieve the List of Features Assigned to a User for Mode Management.

        Retrieve a list of feature identifiers that are already assigned to a user for `Mode Management`. Feature
        identifiers reference feature instances like `Auto Attendants`, `Call Queues`, and `Hunt Groups`.
        A maximum of 50 features can be assigned to a user for `Mode Management`.

        Features with mode-based call forwarding enabled can be assigned to a user for `Mode Management`.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param org_id: Retrieve features list from this organization.
        :type org_id: str
        :rtype: list[UserModeManagementFeatureObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/modeManagement/features')
        data = super().get(url, params=params)
        r = TypeAdapter(list[UserModeManagementFeatureObject]).validate_python(data['features'])
        return r

    def assign_a_list_of_features_to_a_user_for_mode_management_(self, feature_ids: list[str], person_id: str = None,
                                                                 org_id: str = None):
        """
        Assign a List of Features to a User for Mode Management.

        Assign a user a list of feature identifiers for `Mode Management`. Feature identifiers reference feature
        instances like `Auto Attendants`, `Call Queues`, and `Hunt Groups`.
        A maximum of 50 features can be assigned to a user for `Mode Management`.

        Updating mode management settings for a user requires a full, or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param feature_ids: Array of feature IDs.
        :type feature_ids: list[str]
        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param org_id: Retrieve features list from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['featureIds'] = feature_ids
        url = self.ep(f'{person_id}/modeManagement/features')
        super().put(url, params=params, json=body)
