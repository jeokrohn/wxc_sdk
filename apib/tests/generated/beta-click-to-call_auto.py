from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaClicktocallApi']


class BetaClicktocallApi(ApiChild, base='telephony/click2call/callToken'):
    """
    Beta Click-to-call
    
    Click-to-call allows users (guests) who aren't registered as Webex Calling users to easily connect with enterprise
    users.
    Using the web browser, the guest callers can initiate a call without the need to create an account or install an
    additional application.
    The enterprise users can handle click-to-call interactions just like any other calls.
    To initiate a click-to-call interaction, you need to create a `guest token
    <https://developer.webex.com/docs/api/v1/guests-management/create-a-guest>`_ and a call token using the `Service App
    token.
    """

    def create_a_call_token(self, called_number: str, guest_name: str = None) -> str:
        """
        Create a call token

        Create a call token before initiating the click-to-call interaction.
        The call token embeds information related to click-to-call interaction into an encrypted JWE token.
        This token is used along with the `guest token
        <https://developer.webex.com/docs/api/v1/guests-management/create-a-guest>`_ to initialise the `web calling SDK

        Creating a call token requires a service app access token with a scope of `spark:webrtc_calling`.

        :param called_number: Number to be called. This number should be enabled as guest calling destination at
            `Webex Control Hub
            <https://admin.webex.com>`_ by the administrator.
        :type called_number: str
        :param guest_name: Name of the guest caller.
        :type guest_name: str
        :rtype: str
        """
        body = dict()
        body['calledNumber'] = called_number
        if guest_name is not None:
            body['guestName'] = guest_name
        url = self.ep()
        data = super().post(url, json=body)
        r = data['callToken']
        return r
