from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ContactDetails', 'ContactPayload', 'Directory', 'PersonId']


class ContactDetails(ApiModel):
    #: ID of person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNTUyZjY3Yi01OWE5LTQxYmItODczNi0xYjA0MWQxZGRkNWU
    personId: Optional[str] = None
    #: First name of person.
    #: example: John
    firstName: Optional[str] = None
    #: Last name of person.
    #: example: Doe
    lastName: Optional[str] = None
    #: Department ID of person.
    #: example: Y2lzY29zcGFyazovL3VzL0RFUEFSVE1FTlQvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    department: Optional[str] = None
    #: Phone number of person.
    #: example: +12225555309
    phoneNumber: Optional[str] = None
    #: Extension of person.
    #: example: 5309
    extension: Optional[datetime] = None
    #: Location ID of person.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    locationId: Optional[str] = None
    #: Location feature ID of the contact. Supported location feature types are Auto Attendant, Call Queue, Hunt Group, Single Number Reach, and Paging Group.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzA1NTJmNjdiLTU5YTktNDFiYi04NzM2LTFiMDQxZDFkZGQ1ZQ
    featureId: Optional[str] = None


class PersonId(ApiModel):
    #: Person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNTUyZjY3Yi01OWE5LTQxYmItODczNi0xYjA0MWQxZGRkNWU
    personId: Optional[str] = None
    #: Location feature ID.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzA1NTJmNjdiLTU5YTktNDFiYi04NzM2LTFiMDQxZDFkZGQ1ZQ
    featureId: Optional[str] = None
    #: Types of users supported in receptionist contacts are People, Auto Attendant, Call Queue, Hunt Group, Single Number Reach, and Paging Group.
    #: example: PEOPLE
    type: Optional[str] = None


class ContactPayload(ApiModel):
    #: Receptionist Contact Directory name.
    #: example: My_Directory
    name: Optional[str] = None
    #: Array of users assigned to this Receptionist Contact Directory.
    contacts: Optional[list[PersonId]] = None


class Directory(ApiModel):
    #: ID of Receptionist Contact Directory
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZEdWemRGOWthWEpsWTNSdmNuaz06OTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of Receptionist Contact Directory.
    #: example: test_directory
    name: Optional[str] = None
