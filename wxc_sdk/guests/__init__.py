from datetime import datetime, timedelta
from typing import Optional

import pytz

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['Guest', 'GuestManagementApi']


class Guest(ApiModel):
    #: The unique id of the guest. This is a `personId`
    id: Optional[str] = None
    #: The external unique identifier of the guest.
    subject: Optional[str] = None
    #: The guest’s display name shown in Webex applications
    display_name: Optional[str] = None
    #: The person’s synthetic email in Webex.
    email: Optional[str] = None
    #: The guests access token. Guest tokens usually are over 2000 characters in length.
    access_token: Optional[str] = None
    #: The token expiration in seconds from the time of issuance.
    expires_in: Optional[int] = None
    #: absolute time of guest access token expiration
    expires_at: Optional[datetime] = None  #: expiration, calculated at time of guest creation


class GuestManagementApi(ApiChild, base='guests'):
    """
    Guest Management

    Guests in Webex are users with only a temporary identity and are often used for single-transaction collaborations.
    Examples include click-to-call and click-to-chat applications where the guest interacts with the agent only for
    the duration of the call or chat session.
    Guests in Webex are created and managed via a Service App with the scope guest-issuer:write and guest-issuer:read
    and are represented by a token with a fixed and predefined set of scopes.

    Since the Service App manages its own pool of guests, you need to insert the Service App token into the developer
    portal's Try-It mode rather than your default personal token.

    The `guests/token` endpoint is used to create and retrieve guest tokens, and the `guests/count` is used to assess
    the number of current guests.

    Creating guests via the guest-issuer application type is deprecated and will
    be removed in the future.

    """

    def create(self, subject: str, display_name: str) -> Guest:
        """
        Create a Guest

        Create a new token for a single guest user. The Service App that creates the guest must have the scope
        `guest-issuer:write`.

        Guests are implicitly created by retrieving the guest access token.

        Repeated calls to this API with the same `subject` will create additional tokens without invalidating previous
        ones. Tokens are valid until the `expiresIn`.

        Guests can be renamed by supplying the same `subject` and changing the `displayName.`

        To retrieve a new token for an existing guest, please provide the existing guest's `subject`. Tokens are valid
        until `expiresIn`.

        :param subject: The unique and external identifier of the guest.
        :type subject: str
        :param display_name: The display name shown in the Webex application.
        :type display_name: str
        :rtype: :class:`Guest`
        """
        body = dict()
        body['subject'] = subject
        body['displayName'] = display_name
        url = self.ep('token')
        data = super().post(url, json=body)
        guest = Guest.model_validate(data)
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if not guest.expires_at and guest.expires_in:
            delta = timedelta(seconds=guest.expires_in)
            guest.expires_at = now + delta

        return guest

    def guest_count(self) -> int:
        """
        Get Guest Count

        To retrieve the number of guests, the scopes `guest-issuer:read` or `guest-issuer:write` are needed.

        :rtype: int
        """
        url = self.ep('count')
        data = super().get(url)
        return data
