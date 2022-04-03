"""
Telephony types and API
"""

from .calls import CallsApi
from ..common.schedules import ScheduleApi, ScheduleApiBase
from .paging import PagingApi
from .huntgroup import HuntGroupApi
from .callqueue import CallQueueApi
from .callpark import CallParkApi
from .callpickup import CallPickupApi
from .autoattendant import AutoAttendantApi
from ..api_child import ApiChild
from ..rest import RestSession

__all__ = ['TelephonyApi']


class TelephonyApi(ApiChild, base='telephony'):
    """
    The telephony API. Child of :class:`WebexSimpleApi`

    :ivar auto_attendant: :class:`autoattendant.AutoAttendantApi`
    :ivar calls: :class:`calls.CallsApi`
    :ivar schedules: :class:`schedules.ScheduleApi`
    :ivar paging: :class:`paging.PagingApi`
    :ivar huntgroup: :class:`huntgroup.HuntGroupApi`
    :ivar callqueue: :class:`callqueue.CallQueueApi`
    :ivar callpark: :class:`callpark.CallParkApi`
    :ivar pickup: :class:`callpickup.CallPickupApi`

    """

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.auto_attendant = AutoAttendantApi(session=session)
        self.calls = CallsApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.paging = PagingApi(session=session)
        self.huntgroup = HuntGroupApi(session=session)
        self.callqueue = CallQueueApi(session=session)
        self.callpark = CallParkApi(session=session)
        self.pickup = CallPickupApi(session=session)
