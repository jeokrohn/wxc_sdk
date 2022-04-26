"""
Organisation voicemail settings
"""
from typing import Optional

from ..api_child import ApiChild
from ..base import ApiModel

__all__ = ['OrganisationVoicemailSettings', 'OrganisationVoicemailSettingsAPI']


class OrganisationVoicemailSettings(ApiModel):
    """
    voicemail settings for and organization.
    """
    #: When enabled, you can set the deletion conditions for expired messages.
    message_expiry_enabled: bool
    #: Number of days after which messages expire.
    number_of_days_for_message_expiry: int
    #: When enabled, all read and unread voicemail messages will be deleted based on the time frame you set. When
    #:  disabled, all unread voicemail messages will be kept.
    strict_deletion_enabled: Optional[bool]
    #: When enabled, people in the organization can configure the email forwarding of voicemails.
    voice_message_forwarding_enabled: Optional[bool]

    @staticmethod
    def default() -> 'OrganisationVoicemailSettings':
        return OrganisationVoicemailSettings(message_expiry_enabled=False,
                                             number_of_days_for_message_expiry=15,
                                             strict_deletion_enabled=False,
                                             voice_message_forwarding_enabled=False)


class OrganisationVoicemailSettingsAPI(ApiChild, base='telephony/config/voicemail/settings'):
    """
    API for Organisation voicemail settings
    """

    def read(self, *, org_id: str = None) -> OrganisationVoicemailSettings:
        """
        Get Voicemail Settings

        Retrieve the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Retrieving organization's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :return: VM settings
        :rtype: OrganisationVoicemailSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        return OrganisationVoicemailSettings.parse_obj(self.get(url, params=params))

    def update(self, *, settings: OrganisationVoicemailSettings, org_id: str = None):
        """
        Update the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Updating organization's voicemail settings requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param settings: new settings
        :type settings: OrganisationVoicemailSettings
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = settings.json()
        self.put(url, data=data, params=params)
