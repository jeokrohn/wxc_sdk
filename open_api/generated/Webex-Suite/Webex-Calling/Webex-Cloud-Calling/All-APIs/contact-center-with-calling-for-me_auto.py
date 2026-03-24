import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ContactCenterExtensionsGetObject', 'ContactCenterWithCallingForMeApi', 'EndpointStatus', 'EndpointType',
           'ExtensionType', 'LineOwnerType', 'UserEndpointType', 'UserEndpoints', 'UserExtensions']


class ExtensionType(str, Enum):
    #: Indicates that the extension is owned by the user.
    primary = 'PRIMARY'
    #: Indicates that the extension is not owned by the user and is a secondary line on one of the users devices.
    secondary = 'SECONDARY'


class LineOwnerType(str, Enum):
    #: The line is owned by a person.
    people = 'PEOPLE'
    #: The line is owned by a workspace.
    place = 'PLACE'
    #: The line is owned by a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class EndpointType(str, Enum):
    #: Endpoint is a calling device.
    calling_device = 'CALLING_DEVICE'
    #: Endpoint is an application.
    application = 'APPLICATION'
    #: Endpoint is a hotdesking guest.
    hotdesking_guest = 'HOTDESKING_GUEST'


class UserEndpointType(ApiModel):
    #: Unique identifier of the endpoint.
    id: Optional[str] = None
    #: Type of the endpoint.
    type: Optional[EndpointType] = None


class UserExtensions(ApiModel):
    #: Direct number of the user.
    direct_number: Optional[str] = None
    #: Extension of the user.
    extension: Optional[str] = None
    #: Type of User Extension.
    type: Optional[ExtensionType] = None
    #: Type of the line owner. Indicates whether the line is owned by a person, workspace, or virtual line.
    line_owner_type: Optional[LineOwnerType] = None
    #: Unique identifier of the line owner.
    line_owner_id: Optional[str] = None
    #: Unique identifier of the set preferred answering endpoint.
    preferred_answering_end_point_id: Optional[str] = None
    #: List of user endpoints with type.
    endpoints: Optional[list[UserEndpointType]] = None


class EndpointStatus(str, Enum):
    #: Device is connected.
    connected = 'CONNECTED'
    #: Device is not connected.
    not_connected = 'NOT_CONNECTED'


class UserEndpoints(ApiModel):
    #: Unique identifier of the endpoint.
    id: Optional[str] = None
    #: Type of the endpoint.
    type: Optional[EndpointType] = None
    #: Name of the endpoint.
    name: Optional[str] = None
    #: SIP Registration status of the device.
    status: Optional[EndpointStatus] = None


class ContactCenterExtensionsGetObject(ApiModel):
    #: List of user extensions.
    cc_extensions: Optional[list[UserExtensions]] = None
    #: List of user endpoints details.
    endpoints: Optional[list[UserEndpoints]] = None


class ContactCenterWithCallingForMeApi(ApiChild, base='telephony/config/people/me/settings/contactCenterExtensions'):
    """
    Contact Center with Calling For Me
    
    Contact center with calling for me APIs allow a person to read their contact center settings.
    
    Viewing extensions require a user auth token with a scope of `spark:telephony_config_read`.
    """

    def read_the_contact_center_extensions(self) -> ContactCenterExtensionsGetObject:
        """
        Read the Contact Center Extensions

        Retrieves the Contact Center phone number, extension, virtual numbers, endpoints, and endpoints registration
        status associated with the authenticated user. This API returns all primary and secondary endpoints, the hot
        desk guest profiles currently hosted on the agent's own devices, if any, and registration status of those
        endpoints. Only virtual line extensions hosted exclusively on the agent's devices and the registration status
        of those virtual line endpoints will be retrieved. Any virtual lines shared with devices not owned by the
        current user will be excluded.

        A Webex Calling Contact Center extension is a calling extension assigned to a user or device within the Webex
        Contact Center for internal dialing.

        This API requires a user auth token with a scope of spark:telephony_config_read.

        :rtype: :class:`ContactCenterExtensionsGetObject`
        """
        url = self.ep()
        data = super().get(url)
        r = ContactCenterExtensionsGetObject.model_validate(data)
        return r
