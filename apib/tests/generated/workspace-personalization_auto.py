from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['WorkspacePersonalizationRequest', 'WorkspacePersonalizationTaskResponse']


class WorkspacePersonalizationRequest(ApiModel):
    #: The user that the device will become personalised for.
    #: example: julie@example.com
    email: Optional[str] = None


class WorkspacePersonalizationTaskResponse(ApiModel):
    #: Describes if the personalization was successful.
    success: Optional[bool] = None
    #: A description of the error will be provided if the personalization was not successful.
    #: example: Device is offline
    error_description: Optional[str] = None


class WorkspacePersonalizationApi(ApiChild, base='workspaces/{workspaceId}'):
    """
    Workspace Personalization
    
    **This API collection applies only to Webex Edge registered devices.**
    
    The Workspace Personalization API is designed to help administrators enable Personal Mode for `Webex Edge
    <https://help.webex.com/en-us/article/cy2l2z/Webex-Edge-for-Devices>`_ registered
    devices. This one-time operation allows for end users to receive calls and meeting notifications directly on their
    device, without needing to pair. This API aids with the process of the migration from on-premise to
    cloud-registered personal mode systems.
    
    For the personalization of a device to be successful, the following requirements must be satisfied:
    
    - The workspace must contain a single, Webex Edge registered, shared mode device.
    
    - The workspace must not have any calendars configured.
    
    - The device belonging to the workspace must be online.
    
    Invoking this API requires the `spark-admin:devices_write`, `spark:xapi_commands`, `spark:xapi_statuses` and
    `Identity:one_time_password` scopes.
    """
    ...