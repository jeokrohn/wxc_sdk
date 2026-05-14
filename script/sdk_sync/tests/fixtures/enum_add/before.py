from wxc_sdk.base import ApiModel  # noqa: F401
from wxc_sdk.base import SafeEnum as Enum


class Color(str, Enum):
    red = 'red'
    green = 'green'
    blue = 'blue'
