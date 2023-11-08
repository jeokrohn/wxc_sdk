from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListPoliciesType', 'Policy', 'PolicyAction', 'PolicyCollectionResponse', 'PolicyType']


class PolicyType(str, Enum):
    default = 'Default'
    #: Default policy for the org.
    default = 'default'
    #: Customized policy for an App.
    custom = 'custom'


class PolicyAction(str, Enum):
    #: Integration usage allowed.
    allow = 'allow'
    #: Integration usage denied.
    deny = 'deny'


class Policy(ApiModel):
    #: A unique identifier for the policy.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    id: Optional[str] = None
    #: The `appId` of the app to which the policy applies.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    app_id: Optional[str] = None
    #: A user-friendly name for the policy.
    #: example: Allow App 123
    name: Optional[str] = None
    #: The `orgId` of the organization to which the policy applies.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY
    org_id: Optional[str] = None
    #: A policy type for the policy.
    #: example: Default
    type: Optional[PolicyType] = None
    #: The `personIds` for the people this policy applies to.
    #: example: ['Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0', 'Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0', 'Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo']
    person_ids: Optional[list[str]] = None
    #: The policy action.
    #: example: allow
    action: Optional[PolicyAction] = None
    #: The date and time the policy was created.
    #: example: 2017-05-10T19:39:27.970Z
    created: Optional[datetime] = None


class PolicyCollectionResponse(ApiModel):
    items: Optional[list[Policy]] = None


class ListPoliciesType(str, Enum):
    default = 'default'
    custom = 'custom'


class PoliciesApi(ApiChild, base='policies'):
    """
    Policies
    
    Policies give organization administrators more control over the integrations available for use within their
    organization. By default, any user can add an integration for use with Webex. To restrict the usage of
    integrations within an organization, create policies to define what is either allowed or disallowed by the
    organization.
    """

    def list_policies(self, type: ListPoliciesType, app_id: list[str] = None, person_id: list[str] = None,
                      org_id: str = None, name: str = None, action: PolicyAction = None, to_: Union[str,
                      datetime] = None, max_: int = None, cursor: str = None,
                      **params) -> Generator[Policy, None, None]:
        """
        List Policies

        List all policies for an organization. Only lists policies for the organization in which the authenticated user
        belongs.
        
        Use query parameters to filter the response. Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param type: List policies which apply to this policy type.
        :type type: ListPoliciesType
        :param app_id: List policies which apply to this app, by ID.
        :type app_id: list[str]
        :param person_id: List policies which apply to this person, by ID.
        :type person_id: list[str]
        :param org_id: List policies which apply to this `orgId`.
        :type org_id: str
        :param name: List policies which apply to this name.
        :type name: str
        :param action: List policies with this action.
        :type action: PolicyAction
        :param to_: List policies created before this date and time.
        :type to_: Union[str, datetime]
        :param max_: Limit the maximum number of policies in the response.
        :type max_: int
        :param cursor: List the next policies after the current cursor.
        :type cursor: str
        :return: Generator yielding :class:`Policy` instances
        """
        ...


    def create_a_policy(self, type: ListPoliciesType, action: PolicyAction, app_id: str = None, name: str = None,
                        person_ids: list[str] = None) -> Policy:
        """
        Create a Policy

        Add a new policy.

        :param type: Specify a policy type.
        :type type: ListPoliciesType
        :param action: Specify policy action.
        :type action: PolicyAction
        :param app_id: Specify the `appId` for the policy.
        :type app_id: str
        :param name: Specify user-friendly name for the policy.
        :type name: str
        :param person_ids: The `personIds` for the individual people this policy applies to.
        :type person_ids: list[str]
        :rtype: :class:`Policy`
        """
        ...


    def get_policy_details(self, policy_id: str) -> Policy:
        """
        Get Policy Details

        Shows details for a policy, by ID.
        
        Specify the policy ID in the `policyId` URI parameter.

        :param policy_id: A unique identifier for the policy.
        :type policy_id: str
        :rtype: :class:`Policy`
        """
        ...


    def update_a_policy(self, policy_id: str, action: PolicyAction, app_id: str = None, name: str = None,
                        person_ids: list[str] = None) -> Policy:
        """
        Update a Policy

        Update details for a policy, by ID.
        
        Specify the policy ID in the `policyId` URI parameter.

        :param policy_id: A unique identifier for the policy.
        :type policy_id: str
        :param action: The policy action.
        :type action: PolicyAction
        :param app_id: The `appId` of the app to which the policy applies.
        :type app_id: str
        :param name: A user-friendly name for the policy.
        :type name: str
        :param person_ids: The `personIds` for the individual people this policy applies to.
        :type person_ids: list[str]
        :rtype: :class:`Policy`
        """
        ...


    def delete_a_policy(self, policy_id: str):
        """
        Delete a Policy

        Delete a policy, by ID.
        
        Specify the policy ID in the `policyId` URI parameter.

        :param policy_id: A unique identifier for the policy.
        :type policy_id: str
        :rtype: None
        """
        ...

    ...