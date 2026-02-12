from typing import Optional

from pydantic import TypeAdapter
from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['AssignedAssistants', 'MeExecutiveApi']

from wxc_sdk.person_settings.executive import ExecAlert, ExecOrAssistant, AssistantSettings, ExecCallFiltering, \
    ExecCallFilteringCriteria, ExecScreening


class AssignedAssistants(ApiModel):
    #: If `true`, the user can opt in or out of the executive assistant pool.
    allow_opt_in_out_enabled: Optional[bool] = None
    #: List of assigned executive assistants.
    assistants: Optional[list[ExecOrAssistant]] = None

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               include={'allow_opt_in_out_enabled': True,
                                        'assistants': {'__all__': {'id': True}}})




class MeExecutiveApi(ApiChild, base='telephony/config/people/me'):
    def alert_settings(self) -> ExecAlert:
        """
        Get User Executive Alert Settings

        Get executive alert settings for the authenticated user.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecAlert`
        """
        url = self.ep('settings/executive/alert')
        data = super().get(url)
        r = ExecAlert.model_validate(data)
        return r

    def update_alert_settings(self, settings: ExecAlert):
        """
        Modify User Executive Alert Settings

        Update executive alert settings for the authenticated user.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Alert settings
        :type settings: ExecAlert
        """
        body = settings.update()
        url = self.ep('settings/executive/alert')
        super().put(url, json=body)

    def assigned_assistants(self) -> AssignedAssistants:
        """
        Get My Executive Assigned Assistants

        Get list of assigned executive assistants for an authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`AssignedAssistants`
        """
        url = self.ep('settings/executive/assignedAssistants')
        data = super().get(url)
        r = AssignedAssistants.model_validate(data)
        return r

    def update_assigned_assistants(self, assigned_assistants: AssignedAssistants):
        """
        Modify My Executive Assigned Assistants

        Update assigned executive assistants for the authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param assigned_assistants: Assigned Assistants
        :type assigned_assistants: AssignedAssistants
        :rtype: None
        """
        body = assigned_assistants.update()
        if assigned_assistants.assistants:
            body['assistantIds'] = [a.id for a in assigned_assistants.assistants]
            body.pop('assistants')
        url = self.ep('settings/executive/assignedAssistants')
        super().put(url, json=body)

    def executive_assistant_settings(self) -> AssistantSettings:
        """
        Get My Executive Assistant Settings

        Get settings for an executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`AssistantSettings`
        """
        url = self.ep('settings/executive/assistant')
        data = super().get(url)
        r = AssistantSettings.model_validate(data)
        return r

    def update_executive_assistant_settings(self, assistant_settings: AssistantSettings):
        """
        Modify My Executive Assistant Settings

        Update Settings for an executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param assistant_settings: My Executive Assistant Settings
        :type assistant_settings: AssistantSettings
        """
        body = assistant_settings.update()
        url = self.ep('settings/executive/assistant')
        super().put(url, json=body)

    def executive_available_assistants(self) -> list[ExecOrAssistant]:
        """
        Get My Executive Available Assistants

        Get a list of available executive assistants for the authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[ExecOrAssistant]
        """
        url = self.ep('settings/executive/availableAssistants')
        data = super().get(url)
        r = TypeAdapter(list[ExecOrAssistant]).validate_python(data['assistants'])
        return r

    def executive_call_filtering_settings(self) -> ExecCallFiltering:
        """
        Get User Executive Call Filtering Settings

        Get executive call filtering settings for the authenticated user.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecCallFiltering`
        """
        url = self.ep('settings/executive/callFiltering')
        data = super().get(url)
        r = ExecCallFiltering.model_validate(data)
        return r

    def update_executive_call_filtering_settings(self, settings: ExecCallFiltering):
        """
        Update User Executive Call Filtering Settings

        Update executive call filtering settings for the authenticated user.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Call Filtering Settings
        :type settings: ExecCallFiltering
        """
        body = settings.update()
        url = self.ep('settings/executive/callFiltering')
        super().put(url, json=body)

    def create_call_filtering_criteria(self, settings: ExecCallFilteringCriteria) -> str:
        """
        Add User Executive Call Filtering Criteria

        Create a new executive call filtering criteria for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to define detailed filter rules for incoming calls. This
        API creates a new filter rule with the specified configuration, including schedule, phone numbers, and call
        routing preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Call Filtering Settings
        :type settings: ExecCallFilteringCriteria
        """
        body = settings.create()
        url = self.ep('settings/executive/callFiltering/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_call_filtering_criteria(self, id: str):
        """
        Delete User Executive Call Filtering Criteria

        Delete a specific executive call filtering criteria for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to manage detailed filter rules for incoming calls. This
        API removes a specific filter rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        super().delete(url)

    def call_filtering_criteria(self, id: str) -> ExecCallFilteringCriteria:
        """
        Get User Executive Call Filtering Criteria Settings

        Get executive call filtering criteria settings for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to retrieve detailed configuration for a specific filter
        rule. This includes schedule settings, phone number filters, and call routing preferences for executive call
        filtering.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :rtype: :class:`ExecCallFilteringCriteria`
        """
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        data = super().get(url)
        r = ExecCallFilteringCriteria.model_validate(data)
        return r

    def update_call_filtering_criteria(self, id: str, settings: ExecCallFilteringCriteria) -> str:
        """
        Update User Executive Call Filtering Criteria Settings

        Update executive call filtering criteria settings for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to modify detailed configuration for a specific filter
        rule. This includes updating schedule settings, phone number filters, and call routing preferences for
        executive call filtering.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :param settings: Call Filtering Settings
        :type settings: ExecCallFilteringCriteria
        :rtype: str
        """
        body = settings.update()
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        data = super().put(url, json=body)
        r = data['id']
        return r

    def screening_settings(self) -> ExecScreening:
        """
        Get User Executive Screening Settings

        Get executive screening settings for the authenticated user.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecScreening`
        """
        url = self.ep('settings/executive/screening')
        data = super().get(url)
        r = ExecScreening.model_validate(data)
        return r

    def update_screening_settings(self, settings: ExecScreening):
        """
        Modify User Executive Screening Settings

        Update executive screening settings for the authenticated user.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Screening Settings
        :type settings: ExecScreening

        """
        body = settings.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep('settings/executive/screening')
        super().put(url, json=body)
