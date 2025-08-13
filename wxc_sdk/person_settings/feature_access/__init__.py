from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['FeatureAccessApi', 'FeatureAccessSettings', 'FeatureAccessLevel', 'UserFeatureAccessSettings']


class FeatureAccessLevel(str, Enum):
    #: User has full access.
    full_access = 'FULL_ACCESS'
    #: User does not have access.
    no_access = 'NO_ACCESS'


class FeatureAccessSettings(ApiModel):
    #: Set whether end users have access to make changes to their `Anonymous call rejection` feature via UserHub, or
    #: other clients (Webex, IP phone, etc.).
    anonymous_call_rejection: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Barge In` feature via UserHub, or other clients
    #: (Webex, IP phone, etc.).
    barge_in: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Block caller ID` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    block_caller_id: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Call forwarding` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    call_forwarding: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Call waiting` feature via UserHub, or other clients
    #: (Webex, IP phone, etc.).
    call_waiting: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Call notify` feature via UserHub, or other clients
    #: (Webex, IP phone, etc.).
    call_notify: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Connected line identity` feature via UserHub, or
    #: other clients (Webex, IP phone, etc.).
    connected_line_identity: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Executive/Executive assistant` feature via UserHub,
    #: or other clients (Webex, IP phone, etc.).
    executive: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Hoteling` feature via UserHub, or other clients
    #: (Webex, IP phone, etc.).
    hoteling: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Priority alert` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    priority_alert: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Selectively accept calls` feature via UserHub, or
    #: other clients (Webex, IP phone, etc.).
    selectively_accept_calls: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Selectively reject calls` feature via UserHub, or
    #: other clients (Webex, IP phone, etc.).
    selectively_reject_calls: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Selectively forward calls` feature via UserHub, or
    #: other clients (Webex, IP phone, etc.).
    selectively_forward_calls: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Sequential ring` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    sequential_ring: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Simultaneous ring` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    simultaneous_ring: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Single number reach` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    single_number_reach: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Voicemail feature` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    voicemail: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Send calls to voicemail` feature via UserHub, or
    #: other clients (Webex, IP phone, etc.).
    send_calls_to_voicemail: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Email a copy of the voicemail message` feature via
    #: UserHub, or other clients (Webex, IP phone, etc.).
    voicemail_email_copy: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Fax messaging` feature via UserHub, or other clients
    #: (Webex, IP phone, etc.).
    voicemail_fax_messaging: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Message storage` feature via UserHub, or other
    #: clients (Webex, IP phone, etc.).
    voicemail_message_storage: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Notifications` feature via UserHub, or other clients
    #: (Webex, IP phone, etc.).
    voicemail_notifications: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Transfer on '0' to another number.` feature via
    #: UserHub, or other clients (Webex, IP phone, etc.).
    voicemail_transfer_number: Optional[FeatureAccessLevel] = None
    #: Set whether end users have access to make changes to their `Allow End User to Generate Activation Codes & Delete
    #: their Phones` feature via UserHub, or other clients (Webex, IP phone, etc.).
    generate_activation_code: Optional[FeatureAccessLevel] = None

    def update(self) -> dict:
        """
        get data for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True)


class UserFeatureAccessSettings(ApiModel):
    #: Set whether end users have organization's settings enabled for the user.
    user_org_settings_permission_enabled: Optional[bool] = None
    user_settings_permissions: Optional[FeatureAccessSettings] = None


class FeatureAccessApi(ApiChild, base='telephony'):
    """
    End user Feature Access API
    """

    def read_default(self) -> FeatureAccessSettings:
        """
        Read Default Feature Access Settings for Person

        Read the default feature access configuration for users in the organization. It allows administrators to review
        the baseline feature availability settings that will be applied to new users by default, ensuring consistency
        in user experience and policy enforcement.

        This API is part of the organizational-level user configuration management for feature access. It is used to
        define the default settings that control which Webex features are enabled or disabled when users are
        provisioned. In Control Hub, this corresponds to the "Default User Settings" under Calling or Telephony,
        providing centralized control over user capabilities across the organization.

        To call this API, an administrator must use a full, or read-only administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :rtype: :class:`FeatureAccessSettings`
        """
        url = self.ep('config/people/settings/permissions')
        data = super().get(url)
        r = FeatureAccessSettings.model_validate(data)
        return r

    def update_default(self, settings: FeatureAccessSettings):
        """
        Update Default Person Feature Access Configuration

        Updates the default feature access configuration for users in the organization. It allows administrators to
        modify the baseline settings that determine which Webex features are enabled or disabled for users by default,
        ensuring new users are provisioned with consistent access controls.

        This API is part of the organization-level user configuration management for feature access. It supports
        defining and updating default settings that apply automatically to all newly onboarded users. In Control Hub,
        this corresponds to the "Default User Settings" section for Calling or Telephony, enabling centralized and
        scalable configuration of user capabilities.

        To use this API, an administrator must authenticate with a full, or device administrator auth token. The token
        must include the `spark-admin:telephony_config_write` scope.

        :param settings: The feature access settings to be updated.
        :type settings: :class:`FeatureAccessSettings`

        :rtype: None
        """
        body = settings.update()
        url = self.ep('config/people/settings/permissions')
        super().put(url, json=body)

    def read(self, person_id: str) -> UserFeatureAccessSettings:
        """
        Read Feature Access Settings for a Person

        Read the feature access configuration for the current user within the organization. It allows administrators to
        read the telephony settings, including device and location configurations, specific to that user’s role and
        access privileges. This API is useful for managing and verifying user-specific feature access within the
        broader telephony system.

        The feature is part of the organization’s telephony configuration management. It provides insight into the
        settings and permissions that control how telephony services are assigned and configured for individual users.
        This functionality is available through the Control Hub and allows for the management of user access to
        various telephony-related features.

        To access this API, the user must possess a full, or read-only administrator role. The authentication token
        used must include the `spark-admin:telephony_config_read` scope, granting the necessary permissions to read
        the telephony configuration for the user in question.

        :param person_id: User ID of the Organization.
        :type person_id: str
        :rtype: :class:`UserFeatureAccessSettings`
        """
        url = self.ep(f'config/people/{person_id}/settings/permissions')
        data = super().get(url)
        r = UserFeatureAccessSettings.model_validate(data)
        return r

    def update(self,
               person_id: str,
               settings: FeatureAccessSettings):
        """
        Update a Person’s Feature Access Configuration

        Update the feature access configuration for the current user within the organization. It enables administrators
        to modify the telephony settings, including device and location configurations, specific to the user’s role
        and access privileges. This API is useful for making adjustments to user-specific feature access within the
        telephony system.

        The feature is part of the organization’s telephony configuration management. It provides control over the
        settings and permissions that govern how telephony services are assigned and configured for individual users.
        This functionality is available through the Control Hub and enables the modification of user access to various
        telephony-related features.

        To use this API, an administrator must authenticate with a full, or device administrator auth token. The
        authentication token used must include the `spark-admin:telephony_config_write` scope, granting the necessary
        permissions to update the telephony configuration for the user in question.


        :param person_id: User ID of the Organization.
        :type person_id: str
        :param settings: The feature access settings to be updated.
        :type settings: :class:`FeatureAccessSettings`
        :rtype: None
        """
        body = settings.update()
        url = self.ep(f'config/people/{person_id}/settings/permissions')
        super().put(url, json=body)

    def reset(self, person_id: str):
        """
        Reset a Person’s Feature Access Configuration to the Organization’s Default Settings

        Reset of a user’s feature access configuration to the organization’s default settings. It ensures that any
        specific feature configurations set by an administrator for an individual user are overridden and replaced
        with the global configuration of the organization. This process helps to maintain consistency in feature
        access across all users, especially when administrators want to ensure that a user is subject to the
        organization's global settings rather than personalized settings.

        The overall feature, managed through the organization's Control Hub, involves the configuration and
        customization of feature access for users. Administrators can tailor these settings to individual users based
        on their roles or needs, but sometimes a global reset to the default configuration is necessary. The reset API
        simplifies this by programmatically resetting a user’s feature access, which can be crucial when managing
        large teams or updating organizational policies that affect user privileges across multiple devices or
        locations.

        To use this API, an administrator must authenticate with a full, or device administrator auth token. This
        ensures the individual has the necessary privileges to make changes to user configurations. Furthermore, the
        authentication token used must include the `spark-admin:telephony_config_write` scope, which grants the
        required permissions to modify the telephony configuration for the user. This combination of roles and scopes
        ensures that only authorized administrators can reset the feature access configuration.

        :param person_id: User ID of the Organization.
        :type person_id: str
        :rtype: None
        """
        url = self.ep(f'config/people/{person_id}/settings/permissions/actions/reset/invoke')
        super().post(url)
