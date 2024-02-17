from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaUserCallSettingsSetVoicemailPasscodeApi']


class BetaUserCallSettingsSetVoicemailPasscodeApi(ApiChild, base='telephony/config/people'):
    """
    Beta User Call Settings Set Voicemail Passcode
    
    Person Call Settings supports modifying voicemail passcode for a specific person.
    
    Modifying the voicemail passcode for a person requires a full administrator, user administrator or location
    administrator auth token with a scope of `spark-admin:telephony_config_write`.
    """

    def modify_a_person_s_voicemail_passcode(self, person_id: str, passcode: str, org_id: str = None):
        """
        Modify a person's voicemail passcode.

        Modifying a person's voicemail passcode requires a full administrator, user administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Modify voicemail passcode for this person.
        :type person_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a person in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.ep(f'{person_id}/voicemail/passcode')
        super().put(url, params=params, json=body)
