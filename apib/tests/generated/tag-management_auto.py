from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CustomerTagsResponse', 'SubscriptionTagsResponse', 'TagsObj', 'TagsRequest']


class TagsObj(ApiModel):
    #: Name of the tag.
    #: example: Tag name
    name: Optional[str] = None
    #: Description of the tag
    #: example: Tag description
    description: Optional[str] = None


class TagsRequest(ApiModel):
    #: An array of tags.
    tags: Optional[list[TagsObj]] = None


class CustomerTagsResponse(ApiModel):
    #: Name of the customer organization.
    #: example: Customer Name
    org_name: Optional[str] = None
    #: The unique identifier for the customer organization.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    org_id: Optional[str] = None
    #: An array of tags.
    #: example: ['Tags1', 'Tags2']
    tags: Optional[list[str]] = None


class SubscriptionTagsResponse(ApiModel):
    #: Name of the customer organization.
    #: example: Customer Name
    org_name: Optional[str] = None
    #: The unique identifier for the customer organization.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    org_id: Optional[str] = None
    #: An array of tags.
    #: example: ['Tags1,Tags2']
    tags: Optional[list[str]] = None
    #: The unique identifier for the subscription.
    #: example: Sub119911
    subscription_id: Optional[str] = None
    #: boolean flag for trial or not.
    #: example: false
    trial: Optional[str] = None
