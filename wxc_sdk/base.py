import base64
import logging
import os
from datetime import datetime
from typing import Optional, Union

from aenum import Enum, extend_enum
from dateutil import tz
from pydantic import BaseModel, ValidationError

__all__ = ['StrOrDict', 'webex_id_to_uuid', 'to_camel', 'ApiModel', 'CodeAndReason', 'ApiModelWithErrors', 'plus1',
           'dt_iso_str', 'SafeEnum', 'enum_str', 'RETRY_429_MAX_WAIT']

StrOrDict = Union[str, dict]

log = logging.getLogger(__name__)

# maximum wait time for 429 retries
RETRY_429_MAX_WAIT = 60


class SafeEnum(Enum):
    """
    A replacement for the standard Enum class which allows dynamic enhancements of enums
    """
    if os.getenv('API_MODEL_ALLOW_EXTRA', 'allow') != 'allow':
        # don't allow dynamic extension of enum
        @classmethod
        def _missing_(cls, value):
            return None
    else:
        # ... while during normal execution simply dynamically enhance the enum
        @classmethod
        def _missing_(cls, value):
            log.warning(f'auto enhancing Enum {cls.__name__}, new value: {value}')
            return extend_enum(cls, value, value)


def enum_str(enum_or_str: Union[Enum, str]) -> str:
    """
    return str value of enum or string

    :param enum_or_str: value to be converted to string
    :return: str representation
    """
    # try to treat as enum
    try:
        return enum_or_str.value
    except AttributeError:
        pass
    # .. and if that fails we assume that we got a string and return just that
    return enum_or_str


def webex_id_to_uuid(webex_id: Optional[str]) -> Optional[str]:
    """
    Convert a webex id as used by the public APIs to a UUID

    :param webex_id: base 64 encoded id as used by public APIs
    :type webex_id: str
    :return: ID in uuid format
    """
    return webex_id and base64.b64decode(f'{webex_id}==').decode().split('/')[-1]


def to_camel(s: str) -> str:
    """
    Convert snake case variable name to camel case
    log_id -> logId

    :param s: snake case variable name
    :return: Camel case name
    """
    return ''.join(w.title() if i else w for i, w in enumerate(s.split('_')))


API_MODEL_ALLOW_EXTRA = os.getenv('API_MODEL_ALLOW_EXTRA', 'allow')


class ApiModel(BaseModel):
    """
    Base for all models used by the APIs
    """

    class Config:
        alias_generator = to_camel  # alias is camelcase version of attribute name
        populate_by_name = True
        #: set to 'allow' by default. Can be overridden by setting environment variable API_MODEL_ALLOW_EXTRA
        extra = API_MODEL_ALLOW_EXTRA
        #: store values instead of enum types
        use_enum_values = True

    def model_dump_json(self, *args, exclude_none=True, by_alias=True, **kwargs) -> str:
        return super().model_dump_json(*args, exclude_none=exclude_none, by_alias=by_alias, **kwargs)

    @classmethod
    def model_validate(cls, obj):
        try:
            r = super().model_validate(obj)
        except ValidationError as e:
            raise e
        return r


class CodeAndReason(ApiModel):
    code: str
    reason: str


class ApiModelWithErrors(ApiModel):
    errors: Optional[dict[str, CodeAndReason]] = None


def plus1(v: Optional[str]) -> str:
    """
    Convert 10D number to +E.164. Can be used as validator
    :param v:
    :return:
    """
    return v and len(v) == 10 and v[0] != '+' and f'+1{v}' or v


def dt_iso_str(dt: datetime, with_msec: bool = True) -> str:
    """
    ISO format datetime as used by Webex API (no time zone, milliseconds)

    :param dt:
    :param with_msec:
    :return:
    """
    dt = dt.astimezone(tz.tzutc())
    dt = dt.replace(tzinfo=None)
    r = f"{dt.isoformat(timespec='milliseconds')}Z"
    if not with_msec:
        r = r[:-5] + 'Z'
    return r
