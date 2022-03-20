"""
Simple implementation of Webex tokens
"""
from pydantic import BaseModel

from typing import Literal, Optional
import datetime
import pytz

__all__ = ['Tokens']


class Tokens(BaseModel):
    """
    Webex tokens
    """
    access_token: Optional[str]  #: access token
    expires_in: Optional[int]  #: remaining lifetime at time of token creation
    expires_at: Optional[datetime.datetime]  #: expiration, calculated at time of token creation
    refresh_token: Optional[str]  #: refresh token
    refresh_token_expires_in: Optional[int]   # remaining lifetime of refresh token at time of token creation
    refresh_token_expires_at: Optional[datetime.datetime]   #: expiration, calculated at time of token creation
    token_type: Optional[Literal['Bearer']]

    def json(self, *args, **kwargs):
        """
        :meta private:
        """
        exclude = kwargs.get('exclude', set())
        exclude.update(('expires_in', 'refresh_token_expires_in'))
        kwargs['exclude'] = exclude
        return super().json(*args, **kwargs)

    def update(self, new_tokes: 'Tokens'):
        """
        Update with values from new tokens

        :param new_tokes: tokens instance to be used as source
        :type new_tokes: Tokens
        """
        self.access_token = new_tokes.access_token
        self.expires_in = new_tokes.expires_in
        self.expires_at = new_tokes.expires_at
        self.refresh_token = new_tokes.refresh_token
        self.refresh_token_expires_in = new_tokes.refresh_token_expires_in
        self.refresh_token_expires_at = new_tokes.refresh_token_expires_at

    def set_expiration(self):
        """
        Set expiration based on current time and expires in values
        """
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        if not self.expires_at:
            delta = datetime.timedelta(seconds=self.expires_in)
            self.expires_at = now + delta
        if not self.refresh_token_expires_at:
            delta = datetime.timedelta(seconds=self.refresh_token_expires_in)
            self.refresh_token_expires_at = now + delta

    @property
    def remaining(self) -> int:
        """
        remaining lifetime in seconds
        """
        if not self.access_token:
            return 0
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        diff = self.expires_at - now
        diff: datetime.timedelta
        diff = int(diff.total_seconds())
        return diff
