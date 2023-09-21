from datetime import datetime
from typing import Optional

from pydantic import Field

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
