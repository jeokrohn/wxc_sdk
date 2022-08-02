"""
Person numbers API
"""
from pydantic import validator, Field

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..common import RingPattern, PatternAction
from typing import Optional

__all__ = ['PersonPhoneNumber', 'PersonNumbers', 'UpdatePersonPhoneNumber', 'UpdatePersonNumbers', 'NumbersApi']


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

    @validator('direct_number', pre=True)
    def validate_direct_number(cls, v):
        # enforce +E.164 numbers
        return v and (v.startswith('+') and v or f'+1{v}')


class PersonNumbers(ApiModel):
    """
    Information about person's phone numbers
    """
    #: To enable/disable distinctive ring pattern that identifies calls coming from a specific phone number.
    distinctive_ring_enabled: bool
    #: Information about the number.
    phone_numbers: list[PersonPhoneNumber]


class UpdatePersonPhoneNumber(ApiModel):
    """
    Information about a phone number
    """
    #: Flag to indicate primary number or not.
    primary: bool = Field(const=False, default=False)
    #: This is either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: PatternAction
    #: Phone numbers that are assigned.
    external: str
    #: Extension that is being assigned.
    extension: Optional[str]
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern]


class UpdatePersonNumbers(ApiModel):
    """
    Information about person's phone numbers
    """
    #: This enable distinctive ring pattern for the person.
    enable_distinctive_ring_pattern: Optional[bool]
    #: Information about the number.
    phone_numbers: list[UpdatePersonPhoneNumber]


class NumbersApi(PersonSettingsApiChild):
    """
    API for person's numbers
    """

    feature = 'numbers'

    # TODO: documentation defect:
    #  https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-additional-settings/get-a-list-of
    #  -phone-numbers-for-a-person
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
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PersonNumbers.parse_obj(self.get(ep, params=params))

    def update(self, *, person_id: str, update: UpdatePersonNumbers, org_id: str = None):
        """
        Assign or unassign alternate phone numbers to a person.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone
        numbers must follow E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        Assigning or Unassigning an alternate phone number to a person requires a full administrator auth token with
        a scope of spark-admin:telephony_config_write.

        :param person_id: Unique identifier of the person.
        :type person_id: str
        :param update: Update to apply
        :type update: :class:`UpdatePersonNumbers`
        :param org_id: organization to work on
        :type org_id: str
        """
        url = self.session.ep(f'telephony/config/people/{person_id}/numbers')
        params = org_id and {'orgId': org_id} or None
        body = update.json()
        self.put(url=url, params=params, data=body)
