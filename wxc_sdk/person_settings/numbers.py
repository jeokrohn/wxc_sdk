"""
Person numbers API
"""

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..common import RingPattern
from typing import Optional

__all__ = ['PersonPhoneNumber', 'PersonNumbers', 'NumbersApi']


class PersonPhoneNumber(ApiModel):
    """
    Information about a phone number
    """
    #: Flag to indicate primary number or not.
    primary: bool
    #: Phone Number.
    direct_number: Optional[str]
    #: Extension
    extension: Optional[str]
    #: Optional ring pattern and this is applicable only for alternate numbers.
    ring_pattern: Optional[RingPattern]


class PersonNumbers(ApiModel):
    """
    Information about person's phone numbers
    """
    #: To enable/disable distinctive ring pattern that identifies calls coming from a specific phone number.
    distinctive_ring_enabled: bool
    #: Information about the number.
    phone_numbers: list[PersonPhoneNumber]


class NumbersApi(PersonSettingsApiChild):
    """
    Api for person's numbers
    """

    feature = 'numbers'

    # TODO: documentation defect:
    #  https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-additional-settings/get-a-list-of-phone-numbers-for-a-person
    #  says the URL is /v1/people/{personId}/numbers
    #  while it actually is /v1/people/{personId}/features/numbers

    def read(self, *, person_id: str, org_id: str = None) -> PersonNumbers:
        """
        Read Do Not Disturb Settings for a Person
        Retrieve a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.
        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
        use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return:
        """
        # ep = self.ep(path=f'{person_id}/numbers')
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PersonNumbers.parse_obj(self.get(ep, params=params))
