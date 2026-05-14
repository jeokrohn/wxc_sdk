from typing import Optional

from wxc_sdk.base import ApiModel


class Widget(ApiModel):
    #: The widget id.
    id: Optional[str] = None
    #: Old description.
    name: Optional[str] = None
