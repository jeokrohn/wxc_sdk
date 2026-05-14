from typing import Optional

from pydantic import field_validator

from wxc_sdk.base import ApiModel


class Widget(ApiModel):
    #: The widget id.
    id: Optional[str] = None
    #: MAC address.
    mac: Optional[str] = None

    @field_validator('mac')
    @classmethod
    def strip_colons(cls, v: str) -> str:
        return v.replace(':', '')
