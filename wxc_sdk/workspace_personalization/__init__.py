from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['WorkspacePersonalizationApi', 'WorkspacePersonalizationTaskResponse']


class WorkspacePersonalizationTaskResponse(ApiModel):
    #: Describes if the personalization was successful.
    success: Optional[bool] = None
    #: A description of the error will be provided if the personalization was not successful.
    error_description: Optional[str] = None


class WorkspacePersonalizationApi(ApiChild, base='workspaces'):
    """
    Workspace Personalization

    **This API collection applies only to Webex Edge registered devices.**

    The Workspace Personalization API is designed to help administrators enable Personal Mode for `Webex Edge
    <https://help.webex.com/en-us/article/cy2l2z/Webex-Edge-for-Devices>`_ registered
    devices. This one-time operation allows for end users to receive calls and meeting notifications directly on their
    device, without needing to pair. This API aids with the process of the migration from on-premise to
    cloud-registered personal mode systems.

    For the personalization of a device to be successful, the following requirements must be satisfied:

    - The workspace must contain a single, Webex Edge registered, shared mode device.

    - The workspace must not have any calendars configured.

    - The device belonging to the workspace must be online.

    Invoking this API requires the `spark-admin:devices_write`, `spark:xapi_commands`, `spark:xapi_statuses` and
    `Identity:one_time_password` scopes.
    """

    def personalize_a_workspace(self, workspace_id: str, email: str):
        """
        Personalize a Workspace

        Initializes the personalization for a given workspace for the user email provided.

        The personalization process is asynchronous and thus a background task is created when this endpoint is
        invoked.
        After successful invocation of this endpoint a personalization task status URL will be returned in the
        `Location` header, which will point to the `Get Personalization Task
        <https://developer.webex.com/docs/api/v1/workspace-personalization/get-personalization-task>`_ endpoint for this workspace.
        The task should be completed in approximately 30 seconds.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param email: The user that the device will become personalised for.
        :type email: str
        :rtype: None
        """
        body = dict()
        body['email'] = email
        url = self.ep(f'{workspace_id}/personalize')
        super().post(url, json=body)

    def get_personalization_task(self, workspace_id: str) -> WorkspacePersonalizationTaskResponse:
        """
        Get Personalization Task

        Returns the status of a personalization task for a given workspace.

        Whilst in progress the endpoint will return `Accepted` and provide a `Retry-After` header indicating the number
        of seconds a client should wait before retrying.

        Upon completion of the task, the endpoint will return `OK` with a body detailing if the personalization was
        successful and an error description if appropriate.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :rtype: :class:`WorkspacePersonalizationTaskResponse`
        """
        url = self.ep(f'{workspace_id}/personalizationTask')
        data = super().get(url)
        r = WorkspacePersonalizationTaskResponse.model_validate(data)
        return r
