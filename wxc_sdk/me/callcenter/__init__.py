from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['MeCallCenterApi', 'MeCallCenterSettings', 'MeCallQueue', 'AgentACDState']


class AgentACDState(str, Enum):
    #: Agent has signed in.
    sign_in = 'SIGN_IN'
    #: Agent has signed out.
    sign_out = 'SIGN_OUT'
    #: Agent is available.
    available = 'AVAILABLE'
    #: Agent is unavailable.
    unavailable = 'UNAVAILABLE'
    #: Agent has wrapped up.
    wrap_up = 'WRAP_UP'


class MeCallQueue(ApiModel):
    #: Unique call queue identifier.
    id: Optional[str] = None
    #: Indicates if the call queue is `normal` or `CxEssentials`.
    has_cx_essentials: Optional[bool] = None
    #: When `true` it indicates agent has joined the call center.
    available: Optional[bool] = None
    #: Call center skill level.
    skill_level: Optional[int] = None
    #: Call center phone number.
    phone_number: Optional[str] = None
    #: Call center extension.
    extension: Optional[str] = None
    #: Determines whether a queue can be joined or not.
    allow_log_off_enabled: Optional[bool] = None


class MeCallCenterSettings(ApiModel):
    agent_acdstate: Optional[AgentACDState] = Field(alias='agentACDState', default=None)
    #: Indicates a list of call centers the agent has joined or may join.
    queues: Optional[list[MeCallQueue]] = None

    def update(self) -> dict:
        """
        Prepare the object for an update operation by converting it to a dictionary.

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               include={'agent_acdstate': True,
                                        'queues': {'__all__': {'id', 'available'}}})


class MeCallCenterApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> MeCallCenterSettings:
        """
        Get My Call Center Settings

        Retrieves the call center settings and list of all call centers the logged in user belongs to.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        The user must have the call center service assigned.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeCallCenterSettings`
        """
        url = self.ep('settings/queues')
        data = super().get(url)
        r = MeCallCenterSettings.model_validate(data)
        return r

    def modify(self, settings: MeCallCenterSettings):
        """
        Modify My Call Center Settings

        Modify the call center settings and availability for an agent in one or more call centers to which the logged
        in user belongs.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        Contains a list specifying the desired availability status of one or more call centers.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: settings
        :type settings: :class:`MeCallCenterSettings`
        """
        body = settings.update()
        url = self.ep('settings/queues')
        super().put(url, json=body)
