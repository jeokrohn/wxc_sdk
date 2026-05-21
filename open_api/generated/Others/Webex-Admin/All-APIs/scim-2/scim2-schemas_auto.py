import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AttributesObject', 'CanonicalValuesObject', 'GetGroupSchemaResponse',
           'GetGroupSchemaResponseUrnietfparamsscimschemascore20Group', 'GetUserSchemaResponse',
           'GetUserSchemaResponseUrnscimschemasextensionciscowebexidentity20User', 'ReferenceTypesObject',
           'SCIM2SchemasApi', 'SubAttributesObject', 'UserAttributesObject']


class ReferenceTypesObject(str, Enum):
    #: Represents a reference to entities or resources that exist outside the current system or organization.
    external = 'external'
    #: Refers to a reference type that identifies a collection of users or entities within a system.
    group = 'Group'
    #: Denotes a reference to an individual who interacts with the system.
    user = 'User'
    #: Indicates a reference to a computing device or automated system.
    machine = 'Machine'


class CanonicalValuesObject(str, Enum):
    #: Represents a set of users or entities.
    group = 'Group'
    #: Denotes an individual with access credentials to interact with a system or application.
    user = 'User'
    #: Refers to a computing device or automated system within a network.
    machine = 'Machine'
    #: Indicates the physical or virtual place where an entity operates.
    location = 'location'
    #: Relates to the dissemination or allocation of resources, tasks, or information within a system.
    distribution = 'distribution'
    #: Represents rules or guidelines which operates within a system or organization.
    policy = 'policy'
    #: A protocol for managing user identities across multiple domains.
    scim = 'SCIM'
    #: Refers to Active Directory, a directory service for Windows domain networks.
    ad = 'AD'
    #: Denotes Azure Active Directory, Microsoft's cloud-based identity and access management service.
    aad = 'AAD'
    #: A platform for delivering telephony and Unified Communications services.
    broadworks = 'BROADWORKS'
    #: A cloud-based identity management service.
    okta = 'OKTA'
    #: Defines a set of permissions or responsibilities assigned to a user or group within a system.
    role = 'role'
    #: An identifier for a user with administrative privileges.
    id_user_admin = 'id_user_admin'
    #: An identifier for an admin with read-only access, unable to make changes.
    id_readonly_admin = 'id_readonly_admin'
    #: An identifier for an admin responsible for managing devices.
    id_device_admin = 'id_device_admin'
    #: An identifier for an admin with full access and privileges within a system.
    id_full_admin = 'id_full_admin'
    #: Denotes an individual with access credentials to interact with a system or application.
    user = 'user'
    #: Represents a unique, non-hierarchical, and unchanging value or setting.
    unique_flat_static = 'unique_flat_static'
    #: Indicates a value or entity that changes or adapts based on conditions or inputs.
    dynamic = 'dynamic'
    #: Refers to non-hierarchical and unchanging data or structure.
    flat_static = 'flat_static'
    #: Implies a hierarchical and unchanging structure or data.
    nested_static = 'nested_static'
    #: transient - Temporary status or condition related to compliance.
    compliance = 'compliance'
    #: transient - Temporary status indicating an action or decision is awaiting completion.
    pending = 'pending'
    #: Status indicating an entity is flagged for deletion but not yet removed.
    marked_deleted = 'marked_deleted'
    #: Denotes temporary or short-lived status or condition.
    transient = 'transient'
    #: transient - Temporary status relating to suspected fraudulent activity.
    fraud = 'fraud'
    #: Status indicating an entity is currently in use or operational.
    active = 'active'
    #: Status indicating an entity is deactivated or not operational.
    disabled = 'disabled'
    #: Status indicating an entity is temporarily inactive or halted.
    suspended = 'suspended'
    #: Relates to integration or interaction with the Facebook platform.
    facebook = 'facebook'
    #: Refers to Office 365, a cloud-based suite of productivity applications from Microsoft.
    o365 = 'O365'
    #: Relates to integration or interaction with Google services or platforms.
    google = 'google'
    #: Cisco Connection Online, a portal for Cisco customers and partners.
    cco = 'cco'
    #: Denotes a business or organizational environment, often large-scale.
    enterprise = 'enterprise'
    #: calling - Refers to telephony services delivered via cloud infrastructure.
    cloud = 'cloud'
    #: room - A virtual space designated for individual use, often for meetings or collaboration.
    personal = 'personal'
    #: A designation that includes all users or entities within a system or context.
    everyone = 'Everyone'
    #: Refers to entities or communications within an organization.
    internal = 'Internal'
    #: Indicates an entity or setting that is not visible or accessible by default.
    hidden = 'Hidden'
    #: Pertains to settings or entities that apply universally across a system or organization.
    global_ = 'Global'
    #: Denotes communication via telephone or telephone numbers.
    phone = 'phone'
    #: upn - User Principal Name used by a partner organization.
    partner = 'partner'
    #: Refers to electronic mail addresses or communications.
    email = 'email'
    #: A specific role related to Cisco Identity.
    ci_role = 'ciRole'
    #: A role associated with a particular service or function within a system.
    service_role = 'serviceRole'
    #: A role with permissions or responsibilities that apply across an entire system or organization.
    global_role = 'globalRole'
    #: A category for values or entities that do not fit predefined categories.
    other = 'other'
    #: Denotes professional or business-related context or communications.
    work = 'work'
    #: Refers to physical or virtual spaces designated for meetings or collaboration.
    room = 'room'
    #: Indicates a residential or personal context or setting.
    home = 'home'
    #: Refers to calls made outside an internal network or organization.
    external_calling = 'external_calling'
    #: A service dedicated to managing voice communications.
    calling_service = 'calling_service'
    #: Additional contact methods or backup communication channels.
    alternate1 = 'alternate1'
    #: Pertains to mobile phones or communications via mobile networks.
    mobile = 'mobile'
    #: A telephone extension associated with a workplace.
    work_extension = 'work_extension'
    #: Refers to facsimile communications or numbers.
    fax = 'fax'
    #: Additional contact methods or backup communication channels.
    alternate2 = 'alternate2'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    qq = 'qq'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    aim = 'aim'
    #: jid - Jabber IDs used within Cisco Unified Communications Manager or Webex platforms.
    cucm = 'cucm'
    #: squared-jid - Jabber IDs used within Cisco Unified Communications Manager or Webex platforms.
    webex = 'webex'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    msn = 'msn'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    xmpp = 'xmpp'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    skype = 'skype'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    gtalk = 'gtalk'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    icq = 'icq'
    #: Denote integration or interaction with various instant messaging or communication platforms.
    yahoo = 'yahoo'
    #: sip-uri - Session Initiation Protocol Uniform Resource Identifier used by Microsoft services.
    microsoft = 'microsoft'
    #: A small image representation of a larger picture.
    thumbnail = 'thumbnail'
    #: Indicates an image or element that can be adjusted in size.
    resizable = 'resizable'
    #: Refers to an image or picture, often used for profile or identification purposes.
    photo = 'photo'


class SubAttributesObject(ApiModel):
    #: The name of the group.
    name: Optional[str] = None
    #: The type of the group.
    type: Optional[str] = None
    #: An array of additional information about reference types of the group.
    reference_types: Optional[list[ReferenceTypesObject]] = None
    #: A boolean value for the group.
    multi_valued: Optional[bool] = None
    #: Description of the group.
    description: Optional[str] = None
    #: A boolean value for the group.
    required: Optional[bool] = None
    #: A boolean value for the group.
    case_exact: Optional[bool] = None
    #: Mutability of the group.
    mutability: Optional[str] = None
    #: Returned value of the group.
    returned: Optional[str] = None
    #: Uniqueness of the group.
    uniqueness: Optional[str] = None
    #: A list of canonical values of this group.
    canonical_values: Optional[list[CanonicalValuesObject]] = None


class AttributesObject(ApiModel):
    #: The name of the group.
    name: Optional[str] = None
    #: The type of the group.
    type: Optional[str] = None
    #: A boolean value for the group.
    multi_valued: Optional[bool] = None
    #: Description of the group.
    description: Optional[str] = None
    #: A boolean value for the group.
    required: Optional[bool] = None
    #: A boolean value for the group.
    case_exact: Optional[bool] = None
    #: Mutability of the group.
    mutability: Optional[str] = None
    #: Returned value of the group.
    returned: Optional[str] = None
    #: Uniqueness of the group.
    uniqueness: Optional[str] = None
    #: This describes the extent or measurement of something from end to end, quantified as 512.
    length: Optional[int] = None
    #: A list of sub-attributes of this group.
    sub_attributes: Optional[list[SubAttributesObject]] = None
    #: This refers to the measurement or magnitude of an object, entity, or dataset, quantified as 500.
    size: Optional[int] = None
    #: A list of canonical values of this group.
    canonical_values: Optional[list[CanonicalValuesObject]] = None


class GetGroupSchemaResponseUrnietfparamsscimschemascore20Group(ApiModel):
    #: A unique identifier for the group.
    id: Optional[str] = None
    #: The name of the group.
    name: Optional[str] = None
    #: Description of the group.
    description: Optional[str] = None
    #: A list of attributes of this group.
    attributes: Optional[list[AttributesObject]] = None


class GetGroupSchemaResponse(ApiModel):
    #: The core extension of SCIM 2.
    urn_ietf_params_scim_schemas_core_2_0_group: Optional[GetGroupSchemaResponseUrnietfparamsscimschemascore20Group] = Field(alias='urn:ietf:params:scim:schemas:core:2.0:Group', default=None)
    #: The core extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_group: Optional[GetGroupSchemaResponseUrnietfparamsscimschemascore20Group] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:Group', default=None)


class UserAttributesObject(ApiModel):
    #: The name of the user.
    name: Optional[str] = None
    #: The type of the user.
    type: Optional[str] = None
    #: An array of additional information about reference types of the group.
    reference_types: Optional[ReferenceTypesObject] = None
    #: A boolean value for the user.
    multi_valued: Optional[bool] = None
    #: Description of the user.
    description: Optional[str] = None
    #: A boolean value for the user.
    required: Optional[bool] = None
    #: A boolean value for the user.
    case_exact: Optional[bool] = None
    #: Mutability of the user.
    mutability: Optional[str] = None
    #: Returned value of the user.
    returned: Optional[str] = None
    #: A list of canonical values of this user.
    canonical_values: Optional[list[CanonicalValuesObject]] = None
    #: Uniqueness of the user.
    uniqueness: Optional[str] = None
    #: A list of sub-attributes of this user.
    sub_attributes: Optional[list[SubAttributesObject]] = None
    #: This refers to the measurement or magnitude of an object, entity, or dataset, quantified as 50.
    size: Optional[int] = None
    #: This describes the extent or measurement of something from end to end, quantified as 128.
    length: Optional[int] = None


class GetUserSchemaResponseUrnscimschemasextensionciscowebexidentity20User(ApiModel):
    #: A unique identifier for the user.
    id: Optional[str] = None
    #: The name of the user.
    name: Optional[str] = None
    #: Description of the user.
    description: Optional[str] = None
    #: A list of attributes of this user.
    attributes: Optional[list[UserAttributesObject]] = None


class GetUserSchemaResponse(ApiModel):
    #: The Cisco extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[GetUserSchemaResponseUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)
    #: The core extension of SCIM 2.
    urn_ietf_params_scim_schemas_core_2_0_user: Optional[GetUserSchemaResponseUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:ietf:params:scim:schemas:core:2.0:User', default=None)
    #: Enterprise extension of SCIM 2.
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[GetUserSchemaResponseUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)


class SCIM2SchemasApi(ApiChild, base='Schemas/SCIM2'):
    """
    SCIM 2 Schemas
    
    This API allows the service client to fetch all the information about schema (`User` or `Group`) from the CI store.
    It also displays all schemas based on a particular `ID` of either `User` schema or `Group` schema.
    """

    def get_group_schema(self) -> GetGroupSchemaResponse:
        """
        Get Group Schema

        This API allows the service client to get all the `Group` schemas information from CI.

        **Authorization:**

        OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:organizations_rw`

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        :rtype: :class:`GetGroupSchemaResponse`
        """
        url = self.ep('Group')
        data = super().get(url)
        r = GetGroupSchemaResponse.model_validate(data)
        return r

    def get_user_schema(self) -> GetUserSchemaResponse:
        """
        Get User Schema

        This API allows the service client to get all the `User` schemas information from CI.

        **Authorization:**

        OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:organizations_rw`

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        :rtype: :class:`GetUserSchemaResponse`
        """
        url = self.ep('User')
        data = super().get(url)
        r = GetUserSchemaResponse.model_validate(data)
        return r

    def get_schema_using_group_schema_id(self,
                                         schema_id: str) -> GetGroupSchemaResponseUrnietfparamsscimschemascore20Group:
        """
        Get Schema using Group Schema ID

        This API allows the service client to get the Group/User Schema using `Schema Id` from CI.

        Example:

        - `urn:ietf:params:scim:schemas:core:2.0:Group` is one of the `Group Schema Id`. Using this particular ID, we
        can fetch all information related to it.

        - `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User` is one of the `User Schema Id`. Using this
        particular ID, we can fetch all information related to it.

        **Authorization:**

        OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:organizations_rw`

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        :param schema_id: The Schema Id of Group/User Schema
        :type schema_id: str
        :rtype: GetGroupSchemaResponseUrnietfparamsscimschemascore20Group
        """
        url = self.ep(f'{schema_id}')
        data = super().get(url)
        r = GetGroupSchemaResponseUrnietfparamsscimschemascore20Group.model_validate(data['urn:ietf:params:scim:schemas:core:2.0:Group'])
        return r
