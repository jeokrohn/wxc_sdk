from typing import Optional

from wxc_sdk.base import ApiModel


class Widget(ApiModel):
    #: The widget id.
    id: Optional[str] = None
    #: New friendly description.
    name: Optional[str] = None
