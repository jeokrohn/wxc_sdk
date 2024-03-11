from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CustomerTagsResponse', 'PartnerTagsApi', 'SubscriptionTagsResponse', 'TagsObj']


class TagsObj(ApiModel):
    #: Name of the tag.
    #: example: Tag name
    name: Optional[str] = None
    #: Description of the tag
    #: example: Tag description
    description: Optional[str] = None


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
    trial: Optional[bool] = None


class PartnerTagsApi(ApiChild, base='partner/tags'):
    """
    Partner Tags
    
    Customer organization tags offer a flexible way of identifying and grouping customer organizations. Tags are
    configured by partners for their customers and are neither visible to other partners nor the customers themselves.
    To manage tags, the user must have a full partner admin or partner admin role. The authorizing admin must grant
    the spark-admin:organizations-read scope for read operations and spark-admin:organizations-write scope for write
    operations.
    """

    def retrieve_all_customer_tags(self, type: str) -> list[TagsObj]:
        """
        Retrieve all customer tags

        Retrieves all tags which are being used by any customer organizations. Once a tag is unassigned from the last
        customer, it is automatically removed and is not returned by this API.
        This API can be used by a partner full admin, a read-only partner, or an partner admin.
        The `type` can have the value ORGANIZATION or SUBSCRIPTION. If not provided, the value is ORGANIZATION

        :param type: List tags associated with an organization.
        :type type: str
        :rtype: list[TagsObj]
        """
        params = {}
        params['type'] = type
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[TagsObj]).validate_python(data)
        return r

    def create_or_replace_existing_customer_tags_with_the_provided_ones(self, org_id: str,
                                                                        tags: list[TagsObj]) -> list[TagsObj]:
        """
        Create or Replace existing customer tags with the provided ones

        Assign or replace tag(s) which for a customer organization. If the tag doesn't already exist, a new one is
        created and assigned to the customer automatically.
        This API can be used by partner full admins and partner admins.
        Each tag has a character limit of 25. Currently, there is a limit of 5 tags per organization when creating
        tags. To remove all the tags, pass an empty array.
        Specify the customer organization ID in the `orgId` parameter in the URI.

        :param org_id: The unique identifier for the customer organization.
        :type org_id: str
        :param tags: An array of tags.
        :type tags: list[TagsObj]
        :rtype: list[TagsObj]
        """
        body = dict()
        body['tags'] = TypeAdapter(list[TagsObj]).dump_python(tags, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'organizations/{org_id}/assignTags')
        data = super().post(url, json=body)
        r = TypeAdapter(list[TagsObj]).validate_python(data)
        return r

    def get_customer_organization_s_tags(self, org_id: str) -> CustomerTagsResponse:
        """
        Get customer organization's tags

        Retrieve tags associated with a customer organization based on the `orgId` provided.
        This API can be used by a partner full admin, a read-only partner, or an partner admin.
        Specify the customer orgId in the `orgId` parameter in the URI.

        :param org_id: Fetch all customers and associated tags for the customer.
        :type org_id: str
        :rtype: :class:`CustomerTagsResponse`
        """
        url = self.ep(f'organizations/{org_id}')
        data = super().get(url)
        r = CustomerTagsResponse.model_validate(data)
        return r

    def fetch_all_customers_for_a_given_set_of_tags(self, tags: str, max_: int = None) -> list[CustomerTagsResponse]:
        """
        Fetch all customers for a given set of tags

        For a set of tags, retrieve all customer organizations that match any one of the tags.
        This API can be used by a partner full admin, a read-only partner, or an partner admin.

        :param tags: A comma separated list of tags to filter by.
        :type tags: str
        :param max_: Value must be between 1 and 100, inclusive.
        :type max_: int
        :rtype: list[CustomerTagsResponse]
        """
        params = {}
        params['tags'] = tags
        if max_ is not None:
            params['max'] = max_
        url = self.ep('organizations')
        data = super().get(url, params=params)
        r = TypeAdapter(list[CustomerTagsResponse]).validate_python(data)
        return r

    def create_or_replace_existing_subscription_tags_with_the_provided_ones(self, org_id: str, subscription_id: str,
                                                                            tags: list[TagsObj]) -> list[TagsObj]:
        """
        Create or Replace existing subscription tags with the provided ones

        Assign or replace tags specific to each subscription for an organization. Each organization may have one or
        more subscriptions.
        This API can be used by partner full admins and partner admins.
        Currently there is a limit of 5 tags per subscription when creating tags. To remove all the tags, pass an empty
        array.
        Specify the customer organization ID in the `orgId` parameter in the URI and subscription ID in
        `subscriptionId` parameter

        :param org_id: The unique identifier for the customer organization.
        :type org_id: str
        :param subscription_id: The unique identifier for the subscription.
        :type subscription_id: str
        :param tags: An array of tags.
        :type tags: list[TagsObj]
        :rtype: list[TagsObj]
        """
        body = dict()
        body['tags'] = TypeAdapter(list[TagsObj]).dump_python(tags, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'organizations/{org_id}/subscriptions/{subscription_id}/assignTags')
        data = super().post(url, json=body)
        r = TypeAdapter(list[TagsObj]).validate_python(data)
        return r

    def subscription_list_on_a_given_tag_name_or_a_set_of_tags(self, tags: str,
                                                               max_: int = None) -> list[SubscriptionTagsResponse]:
        """
        Subscription List on a given tag name or a set of tags

        For a partner organization fetch all it's subscriptions with their tag list for a given tag names.
        This API can be used by partner full admins, partner admins and admin read-only partners.

        :param tags: A comma separated list of tags to filter by.
        :type tags: str
        :param max_: Value must be between 1 and 100, inclusive.
        :type max_: int
        :rtype: list[SubscriptionTagsResponse]
        """
        params = {}
        params['tags'] = tags
        if max_ is not None:
            params['max'] = max_
        url = self.ep('subscriptions')
        data = super().get(url, params=params)
        r = TypeAdapter(list[SubscriptionTagsResponse]).validate_python(data)
        return r

    def fetch_a_subscription(self, org_id: str, subscription_id: str) -> SubscriptionTagsResponse:
        """
        Fetch a Subscription

        For a given partner org, customer org and external subscription id, fetch subscription details with its
        associated tags.
        This API can be used by partner full admins, partner admins and admin read-only partners.

        :param org_id: The unique identifier for the customer organization.
        :type org_id: str
        :param subscription_id: The unique identifier for the subscription.
        :type subscription_id: str
        :rtype: :class:`SubscriptionTagsResponse`
        """
        url = self.ep(f'organizations/{org_id}/subscriptions/{subscription_id}')
        data = super().get(url)
        r = SubscriptionTagsResponse.model_validate(data)
        return r
