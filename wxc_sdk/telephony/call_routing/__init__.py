from dataclasses import dataclass

from wxc_sdk.api_child import ApiChild
from wxc_sdk.telephony.call_routing.translation_pattern import TranslationPatternsApi
from ...rest import RestSession

__all__ = ['CallRoutingApi']


@dataclass(init=False)
class CallRoutingApi(ApiChild, base='telephony/config'):
    """
    Call Routing Api
    """
    #: translation patterns
    tp: TranslationPatternsApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.tp = TranslationPatternsApi(session=session)
