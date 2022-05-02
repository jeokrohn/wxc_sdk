import base64
import sys
from typing import Optional, Union

from pydantic import BaseModel, ValidationError

__all__ = ['StrOrDict', 'webex_id_to_uuid', 'to_camel', 'ApiModel', 'CodeAndReason', 'ApiModelWithErrors']

StrOrDict = Union[str, dict]


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


class ApiModel(BaseModel):
    """
    Base for all models used by the APIs
    """

    class Config:
        alias_generator = to_camel  # alias is camelcase version of attribute name
        allow_population_by_field_name = True
        #: set to 'forbid' if run in unittest to catch schema issues during tests
        #: else set to 'allow'
        extra = 'forbid' if 'unittest' in sys.modules or 'pytest' in sys.modules else 'allow'

    def json(self, *args, exclude_none=True, by_alias=True, **kwargs) -> str:
        return super().json(*args, exclude_none=exclude_none, by_alias=by_alias, **kwargs)

    @classmethod
    def parse_obj(cls, obj):
        try:
            r = super().parse_obj(obj)
        except ValidationError as e:
            raise e
        return r


class CodeAndReason(ApiModel):
    code: str
    reason: str


class ApiModelWithErrors(ApiModel):
    errors: Optional[dict[str, CodeAndReason]]
