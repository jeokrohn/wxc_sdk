from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesVirtualExtensionsApi', 'GetVirtualExtensionObject', 'GetVirtualExtensionObjectLevel']


class GetVirtualExtensionObjectLevel(str, Enum):
    location = 'LOCATION'


class GetVirtualExtensionObject(ApiModel):
    #: ID of the virtual extension.
    #: example: Y2lzY29zcGFyazovL3VzL1ZJUlRVQUxfRVhURU5TSU9OLzZkNmYwNmVlLTdkNDEtNDQ4Yy05MjgwLWZkM2ZiMDhmOGUyMA
    id: Optional[str] = None
    #: Extension of the virtual extension.
    #: example: 5001
    extension: Optional[str] = None
    #: Routing prefix of the virtual extension's location.
    #: example: 4321
    routing_prefix: Optional[str] = None
    #: ESN of the virtual extension.
    #: example: 43215001
    esn: Optional[str] = None
    #: Directory number of the virtual extension.
    #: example: +6692515287
    phone_number: Optional[str] = None
    #: First name of the virtual extension.
    #: example: John
    first_name: Optional[str] = None
    #: last name of the virtual extension.
    #: example: John
    last_name: Optional[str] = None
    #: Level of the virtual extension. It can be either `ORGANIZATION` or `LOCATION`.
    #: 
    #: +locationId: `Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2QzYjA4MGMwLWU1MjctNDQ1Zi04NTk5LTU5OWJmNzQ2MjViNg` (string,
    #: optional) - ID of the location to which the virtual extension is assigned. The location ID is a unique
    #: identifier for the location in Webex Calling.
    #: +locationName: `Test1` (string, optional) - Name of the location to which the virtual extension is assigned.
    #: example: LOCATION
    level: Optional[GetVirtualExtensionObjectLevel] = None
    #: Display name of the virtual extension.
    #: example: John Smith
    display_name: Optional[str] = None


class BetaFeaturesVirtualExtensionsApi(ApiChild, base='telephony/config/virtualExtensions'):
    """
    Beta Features: Virtual Extensions
    
    Features: Virtual Extensions allow assigning extensions to frequently called external numbers for simplified
    dialing within Webex Calling.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def create_a_virtual_extension(self, display_name: str, phone_number: str, extension: str, first_name: str = None,
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
        `spark-admin:telephony_config_write`.

        :param display_name: Display name of the virtual extension.
        :type display_name: str
        :param phone_number: Directory number of the virtual extension.
        :type phone_number: str
        :param extension: Extension of the virtual extension.
        :type extension: str
        :param first_name: First name of the virtual extension.
        :type first_name: str
        :param last_name: Last name of the virtual extension.
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
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_a_virtual_extension(self, extension_id: str, org_id: str = None) -> GetVirtualExtensionObject:
        """
        Get a Virtual Extension

        Retrieve Virtual Extension details for the given extension ID.

        Retrieving a Virtual Extension requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param extension_id: ID of the virtual extension.
        :type extension_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: :class:`GetVirtualExtensionObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{extension_id}')
        data = super().get(url, params=params)
        r = GetVirtualExtensionObject.model_validate(data)
        return r
