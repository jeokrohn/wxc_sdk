from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AssistantSkillsServiceAPIApi']


class AssistantSkillsServiceAPIApi(ApiChild, base=''):
    """
    Assistant Skills Service API
    
    Develop custom skills to use with the Webex Assistant.
    
    ## Authentication
    
    Uses OAuth v2 Bearer Token / Personal Access Token for its authentication.
    """
