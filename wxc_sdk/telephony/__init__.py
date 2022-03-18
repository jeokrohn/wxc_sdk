"""
Telephony types and API
"""

from .calls import CallsApi
from .schedules import ScheduleAPI
from .paging import PagingAPI
from .huntgroup import HuntGroupAPI
from .callqueue import CallQueueAPI
from ..api_child import ApiChild
from ..rest import RestSession

__all__ = ['TelephonyApi']


class TelephonyApi(ApiChild, base='telephony'):
    """
    The telephony API. Child of :class:`WebexSimpleApi`
    
    :ivar calls: :class:`calls.CallsApi`
    :ivar schedules: :class:`schedules.ScheduleAPI`
    :ivar paging: :class:`paging.PagingAPI`
    :ivar huntgroup: :class:`huntgroup.HuntGroupAPI`
    :ivar callqueue: :class:`callqueue.CallQueueAPI`

    """

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.calls = CallsApi(session=session)
        self.schedules = ScheduleAPI(session=session)
        self.paging = PagingAPI(session=session)
        self.huntgroup = HuntGroupAPI(session=session)
        self.callqueue = CallQueueAPI(session=session)
