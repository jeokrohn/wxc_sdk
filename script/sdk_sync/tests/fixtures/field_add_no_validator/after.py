from typing import Optional

from wxc_sdk.base import ApiModel


class Widget(ApiModel):
    #: The widget id.
    id: Optional[str] = None
    #: The widget name.
    name: Optional[str] = None
    #: The widget color.
    color: Optional[str] = None
