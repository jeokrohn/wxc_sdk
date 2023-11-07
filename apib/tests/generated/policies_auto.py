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
    ...