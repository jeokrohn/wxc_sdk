"""
Customer Experience Essentials Wrap Up Reasons API
"""
from typing import Optional, List

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['WrapupReasonApi', 'QueueWrapupReasonSettings', 'WrapUpReasonDetails', 'WrapupReasonQueue',
           'AvailableQueue',
           'WrapUpReason']


class WrapUpReason(ApiModel):
    #: Unique wrap-up identifier.
    id: Optional[str] = None
    #: Name of the wrap-up reason.
    name: Optional[str] = None
    #: Description of the wrap-up reason.
    description: Optional[str] = None
    #: Number of queues assigned to the wrap-up reason.
    number_of_queues_assigned: Optional[int] = None


class QueueSettingsReason(ApiModel):
    #: Unique wrap-up identifier.
    id: Optional[str] = None
    #: Name of the wrap-up reason.
    name: Optional[str] = None
    #: Description of the wrap-up reason.
    description: Optional[str] = None
    #: Denotes whether the wrap-up reason is the default for the queue.
    default_enabled: Optional[bool] = None


class QueueWrapupReasonSettings(ApiModel):
    #: Denotes whether the wrap-up timer is enabled.
    wrapup_timer_enabled: Optional[bool] = None
    #: Wrap up timer value in seconds.
    wrapup_timer: Optional[int] = None
    #: List of wrap-up reasons.
    wrapup_reasons: Optional[list[QueueSettingsReason]] = None


class WrapupReasonQueue(ApiModel):
    #: Unique queue identifier.
    id: Optional[str] = None
    #: Name of the queue.
    name: Optional[str] = None
    #: Name of the location.
    location_name: Optional[str] = None
    #: Phone number of the queue.
    phone_number: Optional[str] = None
    #: Extension of the queue.
    extension: Optional[int] = None
    #: Denotes whether the default wrap-up is enabled for the queue.
    default_wrapup_enabled: Optional[bool] = None


class WrapUpReasonDetails(ApiModel):
    #: Name of the wrap-up reason.
    name: Optional[str] = None
    #: Description of the wrap-up reason.
    description: Optional[str] = None
    #: Number of queues assigned to the wrap-up reason.
    default_wrapup_queues_count: Optional[int] = None
    #: List of queues assigned to the wrap-up reason.
    queues: Optional[list[WrapupReasonQueue]] = None


class AvailableQueue(ApiModel):
    #: Unique queue identifier.
    id: Optional[str] = None
    #: Name of the queue.
    name: Optional[str] = None
    #: Name of the location.
    location_name: Optional[str] = None
    #: Unique location identifier.
    location_id: Optional[str] = None
    #: Phone number of the queue.
    phone_number: Optional[str] = None
    #: Extension of the queue.
    extension: Optional[int] = None


class WrapupReasonApi(ApiChild, base='telephony/config'):
    """
    Wrap up reasons API
    """

    def read_queue_settings(self, location_id: str, queue_id: str) -> QueueWrapupReasonSettings:
        """
        Read Wrap Up Reason Settings

        Return a wrap-up reason by location ID and queue ID.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the wrap-up reason by location ID and queue ID requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param location_id: The location ID.
        :type location_id: str
        :param queue_id: The queue ID.
        :type queue_id: str
        :rtype: list[QueueWrapupReasonSettings]
        """
        url = self.ep(f'cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings')
        data = super().get(url)
        return QueueWrapupReasonSettings.model_validate(data)

    def update_queue_settings(self, location_id: str, queue_id: str, wrapup_reasons: list[str] = None,
                              default_wrapup_reason_id: str = None, wrapup_timer_enabled: bool = None,
                              wrapup_timer: int = None):
        """
        Update Wrap Up Reason Settings

        Modify a wrap-up reason by location ID and queue ID.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Modifying a wrap-up reason by location ID and queue ID requires a full or device administrator auth token with
        a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID.
        :type location_id: str
        :param queue_id: The queue ID.
        :type queue_id: str
        :param wrapup_reasons: List of wrap-up reason IDs.
        :type wrapup_reasons: list[str]
        :param default_wrapup_reason_id: Unique wrap-up identifier. To clear the default wrap-up reason, set this to ''.
        :type default_wrapup_reason_id: str
        :param wrapup_timer_enabled: Denotes whether the wrap-up timer is enabled.
        :type wrapup_timer_enabled: bool
        :param wrapup_timer: Wrap up timer value in seconds.
        :type wrapup_timer: int
        :rtype: None
        """
        body = dict()
        if wrapup_reasons is not None:
            body['wrapupReasons'] = wrapup_reasons
        if default_wrapup_reason_id is not None:
            body['defaultWrapupReasonId'] = default_wrapup_reason_id or None
        if wrapup_timer_enabled is not None:
            body['wrapupTimerEnabled'] = wrapup_timer_enabled
        if wrapup_timer is not None:
            body['wrapupTimer'] = wrapup_timer
        url = self.ep(f'cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings')
        super().put(url, json=body)

    def list(self) -> List[WrapUpReason]:
        """
        List Wrap Up Reasons

        Return the list of wrap-up reasons configured for a customer.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues. Upon call completion, agents select a
        wrap-up reason from the queue's assigned list. Each wrap-up reason includes a name and description, and can be
        set as the default for a queue. Admins can also configure a timer, which dictates the time agents have to
        select a reason post-call, with a default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the list of wrap-up reasons requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :rtype: list[WrapUpReason]
        """
        url = self.ep('cxEssentials/wrapup/reasons')
        data = super().get(url)
        r = TypeAdapter(list[WrapUpReason]).validate_python(data['wrapupReasons'])
        return r

    def create(self, name: str, description: str = None, queues: List[str] = None,
               assign_all_queues_enabled: bool = None) -> str:
        """
        Create Wrap Up Reason

        Create a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Creating a wrap-up reason requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: Name of the wrap-up reason.
        :type name: str
        :param description: Description of the wrap-up reason.
        :type description: str
        :param queues: List of queue IDs assigned to the wrap-up reason.
        :type queues: list[str]
        :param assign_all_queues_enabled: Denotes whether all queues are assigned to the wrap-up reason.
        :type assign_all_queues_enabled: bool
        :return: Wrap-up reason ID.
        :rtype: str
        """
        body = dict()
        body['name'] = name
        if description is not None:
            body['description'] = description
        if queues is not None:
            body['queues'] = queues
        if assign_all_queues_enabled is not None:
            body['assignAllQueuesEnabled'] = assign_all_queues_enabled
        url = self.ep('cxEssentials/wrapup/reasons')
        data = super().post(url, json=body)
        return data['id']

    def validate(self, name: str):
        """
        Validate Wrap Up Reason

        Validate the wrap-up reason name.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Validating the wrap-up reason name requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: Name of the wrap-up reason.
        :type name: str
        :rtype: None
        """
        body = dict()
        body['name'] = name
        url = self.ep('cxEssentials/wrapup/reasons/actions/validateName/invoke')
        super().post(url, json=body)

    def delete(self, wrapup_reason_id: str):
        """
        Delete Wrap Up Reason

        Delete a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Deleting the wrap-up reason requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :rtype: None
        """
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}')
        super().delete(url)

    def details(self, wrapup_reason_id: str) -> WrapUpReasonDetails:
        """
        Read Wrap Up Reason

        Return the wrap-up reason by ID.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the wrap-up reason by ID requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :rtype: WrapUpReasonDetails
        """
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}')
        data = super().get(url)
        r = WrapUpReasonDetails.model_validate(data)
        return r

    def update(self, wrapup_reason_id: str, name: str = None, description: str = None,
               queues_to_assign: List[str] = None, queues_to_unassign: List[str] = None,
               assign_all_queues_enabled: bool = None, unassign_all_queues_enabled: bool = None):
        """
        Update Wrap Up Reason

        Modify a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Modifying a wrap-up reason requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :param name: Name of the wrap-up reason.
        :type name: str
        :param description: Description of the wrap-up reason.
        :type description: str
        :param queues_to_assign: List of queue IDs to assign to the wrap-up reason.
        :type queues_to_assign: list[str]
        :param queues_to_unassign: List of queue IDs to unassign from the wrap-up reason.
        :type queues_to_unassign: list[str]
        :param assign_all_queues_enabled: Denotes whether all queues are assigned to the wrap-up reason.
        :type assign_all_queues_enabled: bool
        :param unassign_all_queues_enabled: Denotes whether all queues are unassigned from the wrap-up reason.
        :type unassign_all_queues_enabled: bool
        :rtype: None
        """
        body = dict()
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if queues_to_assign is not None:
            body['queuesToAssign'] = queues_to_assign
        if queues_to_unassign is not None:
            body['queuesToUnassign'] = queues_to_unassign
        if assign_all_queues_enabled is not None:
            body['assignAllQueuesEnabled'] = assign_all_queues_enabled
        if unassign_all_queues_enabled is not None:
            body['unassignAllQueuesEnabled'] = unassign_all_queues_enabled
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}')
        super().put(url, json=body)

    def available_queues(self, wrapup_reason_id: str) -> List[AvailableQueue]:
        """
        Read Available Queues

        Return the available queues for a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.

        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.

        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the available queues for a wrap-up reason requires a full or read-only administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :rtype: list[AvailableQueue]
        """
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}/availableQueues')
        data = super().get(url)
        if 'queues' not in data:
            return []
        r = TypeAdapter(list[AvailableQueue]).validate_python(data['queues'])
        return r
