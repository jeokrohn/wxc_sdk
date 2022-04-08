"""
Telephony types and API
"""
from dataclasses import dataclass

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


@dataclass(init=False)
class TelephonyApi(ApiChild, base='telephony'):
    """
    The telephony settings (features) API.

    """
    auto_attendant: AutoAttendantApi
    calls: CallsApi
    schedules: ScheduleApi
    paging: PagingApi
    huntgroup: HuntGroupApi
    callqueue: CallQueueApi
    callpark: CallParkApi
    pickup: CallPickupApi

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
