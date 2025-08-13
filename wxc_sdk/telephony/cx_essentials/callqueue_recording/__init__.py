from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings.call_recording import CallRecordingSetting

__all__ = ['QueueCallRecordingSettingsApi']


class QueueCallRecordingSettingsApi(ApiChild, base='telephony/config/locations'):
    """
    Queue Call Recording Settings

    Queue Call Settings supports modifying Webex Calling settings for a specific queue.

    Viewing Queue recording settings requires a full, user, or read-only administrator or location administrator auth
    token with a scope of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read`
    scope can be used by a person to read their own settings.

    Configuring Queue recording settings requires a full or user administrator or location administrator auth token
    with the `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope
    can be used by a person to update their own settings.

    Call Queue Recording Settings API access can be restricted via Control Hub by a full administrator. Restricting
    access causes the APIs to throw a `403 Access Forbidden` error.

    See details about `features available by license type for Webex Calling
    <https://help.webex.com/en-us/article/n1qbbp7/Features-available-by-license-type-for-Webex-Calling>`_.
    """

    def read(self, location_id: str, queue_id: str,
             org_id: str = None) -> CallRecordingSetting:
        """
        Read Queue Call Recording Settings for a Queue

        Retrieve a queue's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        A person with a Webex Calling Standard license is eligible for the Call Recording
        feature only when the Call Recording vendor is Webex.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param queue_id: Unique identifier for the queue.
        :type queue_id: str
        :param org_id: ID of the organization in which the queue resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallRecordingSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/queues/{queue_id}/cxEssentials/callRecordings')
        data = super().get(url, params=params)
        r = CallRecordingSetting.model_validate(data)
        return r

    def configure(self, location_id: str, queue_id: str,
                  recording: CallRecordingSetting,
                  org_id: str = None):
        """
        Configure Queue Call Recording Settings for a Queue

        Configure a queue's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        <div><Callout type="warning">A person with a Webex Calling Standard license is eligible for the Call Recording
        feature only when the Call Recording vendor is Webex.</Callout></div>

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param queue_id: Unique identifier for the queue.
        :type queue_id: str
        :param recording: the new recording settings
        :type recording: CallRecordingSetting
        :param org_id: ID of the organization in which the queue resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = recording.update()
        url = self.ep(f'{location_id}/queues/{queue_id}/cxEssentials/callRecordings')
        super().put(url, params=params, json=body)
