from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Organization', 'OrganizationCollectionResponse']


class Organization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    id: Optional[str] = None
    #: Full name of the organization.
    #: example: Acme, Inc.
    display_name: Optional[str] = None
    #: The date and time the organization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None


class OrganizationCollectionResponse(ApiModel):
    items: Optional[list[Organization]] = None


class OrganizationsApi(ApiChild, base='organizations'):
    """
    Organizations
    
    A set of people in Webex. Organizations may manage other organizations or be managed themselves. This organizations
    resource can be accessed only by an admin.
    
    Applications can delete an Organization only after they have been authorized by a user with the
    `Full Administrator Role
    <https://help.webex.com/en-us/fs78p5/Assign-Organization-Account-Roles-in-Cisco-Webex-Control-Hub#id_117864>`_ which may be a user in the customer org or a user in a managing partner organization to
    which the role has been granted. The authorizing admin must grant the `spark-admin:organizations-write` scope.
    """
    ...