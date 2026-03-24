import base64
import logging
import os
import re
from datetime import datetime
from typing import Annotated, Any, Optional, Self, TypeVar, Union

from aenum import Enum, extend_enum
from dateutil import tz
from pydantic import BaseModel, BeforeValidator, ConfigDict, ValidationError

__all__ = [
    'StrOrDict',
    'webex_id_to_uuid',
    'to_camel',
    'ApiModel',
    'ApiModelType',
    'CodeAndReason',
    'ApiModelWithErrors',
    'plus1',
    'dt_iso_str',
    'SafeEnum',
    'enum_str',
    'RETRY_429_MAX_WAIT',
    'E164Number',
]

StrOrDict = Union[str, dict[str, Any]]

log = logging.getLogger(__name__)

# maximum wait time for 429 retries
RETRY_429_MAX_WAIT = 60


class SafeEnum(Enum):
    """
    A replacement for the standard Enum class which allows dynamic enhancements of enums
    """

    if os.getenv('API_MODEL_ALLOW_EXTRA', 'allow') != 'allow':
        # don't allow dynamic extension of enum
        # noinspection PyUnusedLocal
        @classmethod
        def _missing_(cls, value: Any) -> None:
            return None
    else:
        # ... while during normal execution simply dynamically enhance the enum
        @classmethod
        def _missing_(cls, value: Any) -> Any:
            log.warning(f'auto enhancing Enum {cls.__name__}, new value: {value}')
            return extend_enum(cls, value, value)


def enum_str(enum_or_str: Union[Enum, str]) -> str:
    """
    return str value of enum or string

    :param enum_or_str: value to be converted to string
    :type enum_or_str: Union[Enum, str]
    :return: str representation
    """
    # try to treat as enum
    try:
        return enum_or_str.value  # type: ignore[no-any-return,union-attr]
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

    model_config = ConfigDict(
        alias_generator=to_camel,  # alias is camelcase version of attribute name
        populate_by_name=True,
        # set to 'allow' by default. Can be overridden by setting environment variable API_MODEL_ALLOW_EXTRA
        extra=API_MODEL_ALLOW_EXTRA,  # type: ignore[typeddict-item]
        # store values instead of enum types
        use_enum_values=True,
    )

    def model_dump_json(self, exclude_none: bool = True, by_alias: bool = True, **kwargs: Any) -> str:  # type: ignore[override]
        return super().model_dump_json(exclude_none=exclude_none, by_alias=by_alias, **kwargs)

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> Self:
        try:
            r = super().model_validate(obj, **kwargs)
        except ValidationError as e:
            raise e
        return r


ApiModelType = TypeVar('ApiModelType', bound='ApiModel')


class CodeAndReason(ApiModel):
    code: str
    reason: str


class ApiModelWithErrors(ApiModel):
    errors: Optional[dict[str, CodeAndReason]] = None


def plus1(v: Optional[str]) -> Optional[str]:
    """
    Convert 10D number to +E.164. Can be used as validator
    :param v:
    :return:
    """
    return v and len(v) == 10 and v[0] != '+' and f'+1{v}' or v


def e164(v: str) -> str:
    if not isinstance(v, str):
        return v
    v = re.sub(r'[^+\d]+', '', v)
    if len(v) == 10 and v[0] != '+':
        # convert 10D to +1<10D>
        v = f'+1{v}' or v
    return v


# +E.164 string: all unwanted characters are removed and 10D converted to +1-10D
E164Number = Annotated[str, BeforeValidator(e164)]


def dt_iso_str(dt: datetime, with_msec: bool = True) -> str:
    """
    ISO format datetime as used by Webex API (no time zone, milliseconds)

    :param dt:
    :param with_msec:
    :return:
    """
    dt = dt.astimezone(tz.tzutc())
    dt = dt.replace(tzinfo=None)
    r = f'{dt.isoformat(timespec="milliseconds")}Z'
    if not with_msec:
        r = r[:-5] + 'Z'
    return r
