from dataclasses import dataclass
from enum import Enum
from typing import List, Union

from wxc_sdk.api_child import ApiChild
from .dial_plan import DialPlanApi
from .route_group import RouteGroupApi
from .route_list import RouteListApi
from .trunk import TrunkApi
from ...base import ApiModel
from ...common import DialPatternValidate
from ...rest import RestSession

__all__ = ['DialPatternValidationStatus', 'DialPatternValidationResult',
           'PremisePstnApi']


class DialPatternValidationStatus(str, Enum):
    """
    Overall validation result status.
    """
    #: In case one or more dial pattern validation failed.
    errors = 'ERRORS'
    #: If all the patterns are validated successfully.
    ok = 'OK'


class DialPatternValidationResult(ApiModel):
    #: Overall validation result status.
    status: DialPatternValidationStatus
    dial_pattern_status: list[DialPatternValidate]

    @property
    def ok(self) -> bool:
        return self.status == DialPatternValidationStatus.ok


@dataclass(init=False)
class PremisePstnApi(ApiChild, base='telephony/config/premisePstn'):
    """
    Premises PSTN API
    """
    #: dial plan configuration
    dial_plan: DialPlanApi
    #: trunk configuration
    trunk: TrunkApi
    #: route group configuration
    route_group: RouteGroupApi
    #: route list configuration
    route_list: RouteListApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.dial_plan = DialPlanApi(session=session)
        self.trunk = TrunkApi(session=session)
        self.route_group = RouteGroupApi(session=session)
        self.route_list = RouteListApi(session=session)

    def validate_pattern(self, dial_patterns: Union[str, List[str]], org_id: str = None) -> DialPatternValidationResult:
        """
        Validate a Dial Pattern.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Validating a dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_patterns: Array of dial patterns.
        :type dial_patterns: list[str] or str
        :param org_id: Organization to which dial plan belongs.
        :return: validation result
        :rtype: :class:`DialPatternValidationResult`
        """
        if isinstance(dial_patterns, str):
            dial_patterns = [dial_patterns]

        url = self.ep('actions/validateDialPatterns/invoke')
        params = org_id and {'orgId': org_id} or None
        body = {'dialPatterns': dial_patterns}
        data = self.post(url=url, params=params, json=body)
        return DialPatternValidationResult.parse_obj(data)
