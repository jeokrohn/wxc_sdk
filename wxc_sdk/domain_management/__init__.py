import builtins
from typing import Any, Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = [
    'DomainManagementApi',
    'ClaimDomain',
    'DomainVerification',
    'DomainVerificationToken',
    'PostDomainVerificationToken',
]


class PostDomainVerificationToken(ApiModel):
    #: A valid domain name.
    domain: Optional[str] = None


class DomainVerificationToken(ApiModel):
    #: The domain name for which the token is generated.
    domain: Optional[str] = None
    #: A token needs to be added as a TXT record in your domain's DNS settings. You should add the following string:
    #: 'cisco-ci-domain-verification=<token>' as a TXT record in your DNS settings.
    token: Optional[str] = None
    #: Domain verification method: Currently, we only support the DNS_TXT method for domain verification.
    verification_method: Optional[str] = None
    #: Use this URL for retrieving an authentication token needed to interact with the Domain Verification API.
    url: Optional[str] = None


class DomainVerification(ApiModel):
    #: A list of verified domains for a given organization.
    verified_domains: Optional[list[str]] = None
    #: A list of claimed domains for a given organization.
    claimed_domains: Optional[list[str]] = None
    #: Use this URL for verifying domain ownership and managing the domain lifecycle within the organization.
    url: Optional[str] = None


class ClaimDomain(ApiModel):
    #: A list of verified domains for a given organizations.
    domain: Optional[str] = None
    #: Use this location URL for the domain resource. The resource component of the URL will be the base64 encoded
    #: domain name.
    url: Optional[str] = None


class DomainManagementApi(ApiChild, base='identity/organizations'):
    """
    API - Domain Management

    Common Identity helps organizations prove they own certain domains. Organizations can verify a domain and claim
    ownership of it. Verifying a domain ensures that a user in a given organization belongs to that specific domain.
    You can verify domains in three steps:

    1. Get a verification token using the 'GetToken' API.

    2. Add the received verification token as a 'TXT' record for the specific domain to your DNS server.

    3. Call the CI API to verify domain ownership.

    4. After verification, you can claim the domain using the 'Claim Domain' API.

    If you need to release previously claimed domains, you can use the 'Unclaim Domain' API. This API lets an
    organization give up its claim on a domain, so the domain won't be marked as 'claimed' by that organization
    anymore.
    However, releasing a claim doesn't change the verification status of the domain.
    Even after being unclaimed, the domain stays verified, showing that its ownership and control were successfully
    validated during the original verification process.

    If you want to remove both the claim and the verification status, you'll need to use a different API. To unverify
    domains for the organization, you can use the 'Unverify' API.
    This API invalidates the domain’s verification, meaning the domain is no longer considered verified by the system.
    """

    def claim_domain(
        self,
        org_id: str,
        data: list[PostDomainVerificationToken] = None,
        force_domain_claim: bool = None,
        claim_domain_only: bool = None,
    ) -> builtins.list[ClaimDomain]:
        """
        Claim Domain

        This endpoint helps claim the given domain within the specified organization. The domain needs to be verified
        before it can be claimed.

        **Note**

        There's an organization-level boolean flag called 'enforceVerifiedDomains'. If this flag is set to false, we
        won't put any user in the organization into a transient state when verifying or claiming a domain.
        Customers can still create users within the organization who don't use the verified domains as their email.
        However, if the flag is set to true, all users in the organization must use one of the verified domains as
        their email.
        This flag defines whether the organization enforces user email verification within the organization. If set to
        true, all users inside the organization must use one of the verified domains.
        This flag is effective only after the admin has verified at least one email domain.

        **Possible Error:**

        - 400: The request was a Bad Request. This error occurs if the domain is not verified.

        **Authorization:**

        An 'OAuth' token issued by the 'Identity Broker' is required to access this endpoint. The token must include
        one of the following scopes:

        - `Identity:Organization`

        - `identity:organizations_rw`

        **Administrator Roles:**

        The following administrators can use this API:

        - `id_full_admin`

        :param org_id: The Webex Identity-assigned organization identifier for a user's organization.
        :type org_id: str
        :param data: A List of valid domain name that is already verified by the organization.
        :type data: list[PostDomainVerificationToken]
        :param force_domain_claim: Indicate if the domain should be claimed when there are users outside the
            organization using the same domain. The default is true.
        :type force_domain_claim: bool
        :param claim_domain_only: Indicate to just claim the domain only without searching/marking external users as
            transient. The default is false.
        :type claim_domain_only: bool
        :rtype: list[ClaimDomain]
        """
        body: dict[str, Any] = dict()
        if data is not None:
            body['data'] = TypeAdapter(list[PostDomainVerificationToken]).dump_python(
                data, mode='json', by_alias=True, exclude_none=True
            )
        if force_domain_claim is not None:
            body['forceDomainClaim'] = force_domain_claim
        if claim_domain_only is not None:
            body['claimDomainOnly'] = claim_domain_only
        url = self.ep(f'{org_id}/actions/claimDomain')
        data = super().post(url, json=body)  # type: ignore[assignment]
        r = TypeAdapter(list[ClaimDomain]).validate_python(data['data'])  # type: ignore[call-overload]
        return r

    def get_domain_verification_token(self, org_id: str, domain: str) -> DomainVerificationToken:
        """
        Get Domain Verification Token

        This endpoint helps generate a token for a given domain within the specified organization. The user needs to
        add this token as a 'TXT' record to the DNS server.

        **Possible Error:**

        - 409: The request encountered a resource conflict. This error occurs if the domain is either claimed by
        another organization or by the same organization.

        **Authorization:**

        An 'OAuth' token issued by the 'Identity Broker' is required to access this endpoint. The token must include
        one of the following scopes:

        - `Identity:Organization`

        - `identity:organizations_rw`

        **Administrator Roles:**

        The following administrators can use this API:

        - `id_full_admin`

        :param org_id: The Webex Identity-assigned organization identifier for a user's organization.
        :type org_id: str
        :param domain: A valid domain name.
        :type domain: str
        :rtype: :class:`DomainVerificationToken`
        """
        body: dict[str, Any] = dict()
        body['domain'] = domain
        url = self.ep(f'{org_id}/actions/getDomainVerificationToken')
        data = super().post(url, json=body)
        r = DomainVerificationToken.model_validate(data)
        return r

    def unclaim_domain(self, org_id: str, domain: str) -> None:
        """
        Unclaim Domain

        This API is used to unclaim a domain for the organization. The domain will remain verified, and domain
        enforcement will still apply to the given organization.

        **Possible Error:**

        - 400: The request was a Bad Request. The domain cannot be unclaimed. This error occurs if the requested
        parameter is invalid.

        **Authorization:**

        An 'OAuth' token issued by the 'Identity Broker' is required to access this endpoint. The token must include
        one of the following scopes:

        - `Identity:Organization`

        - `identity:organizations_rw`

        **Administrator Roles:**

        The following administrators can use this API:

        - `id_full_admin`

        :param org_id: The Webex Identity-assigned organization identifier for a user's organization.
        :type org_id: str
        :param domain: A claimed domain.
        :type domain: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['domain'] = domain
        url = self.ep(f'{org_id}/actions/unclaimDomain')
        super().post(url, json=body)

    def unverify_domain(self, org_id: str, domain: str, remove_pending: bool = None) -> DomainVerification:
        """
        Unverify Domain

        After you unclaim the domain, it will still be verified. Domain enforcement will still apply to the
        organization. The unverify endpoint helps to remove the domain ownership verification for the organization.

        **Possible Error:**

        - 400: The request was a Bad Request. The domain cannot be unverified. This error occurs if the domain is still
        claimed.

        - 404: The request was Not Found. This error occurs if the domain is not associated with the organization.

        **Authorization:**

        An 'OAuth' token issued by the 'Identity Broker' is required to access this endpoint. The token must include
        one of the following scopes:

        - `Identity:Organization`

        - `identity:organizations_rw`

        **Administrator Roles:**

        The following administrators can use this API:

        - `id_full_admin`

        :param org_id: The Webex Identity-assigned organization identifier for a user's organization.
        :type org_id: str
        :param domain: Domain name to be verified.
        :type domain: str
        :param remove_pending: Specify whether to remove pending domain. Default is false (backward compatibility). If
            true, domains will be deleted from pending domain list.
        :type remove_pending: bool
        :rtype: :class:`DomainVerification`
        """
        body: dict[str, Any] = dict()
        body['domain'] = domain
        if remove_pending is not None:
            body['removePending'] = remove_pending
        url = self.ep(f'{org_id}/actions/unverifyDomain')
        data = super().post(url, json=body)
        r = DomainVerification.model_validate(data)
        return r

    def verify_domain(
        self, org_id: str, domain: str, claim_domain: bool = None, reserve_domain: bool = None
    ) -> DomainVerification:
        """
        Verify Domain

        This endpoint helps verify a given domain within the specified organization. This API verifies domain ownership
        by looking up and validating the 'TXT' record for the domain.
        Once verified, domain enforcement will be applied to the organization. Any users in the organization whose
        email domain doesn't match one of the verified domains will be marked as transient.

        If you want to verify and claim the domain, just set the 'claimDomain' parameter to true. By default, it's set
        to false, which will only verify the domain.

        **Possible Errors:**

        - 400: The request was a Bad Request. The domain can't be verified. This error happens if the user didn't
        request a token before trying to verify the domain.

        - 409: The request resulted in a resource conflict. This error occurs if the domain has already been claimed by
        another organization.

        **Authorization:**

        An 'OAuth' token issued by the 'Identity Broker' is required to access this endpoint. The token must include
        one of the following scopes:

        - `Identity:Organization`

        - `identity:organizations_rw`

        **Administrator Roles:**

        The following administrators can use this API:

        - `id_full_admin`

        :param org_id: The Webex Identity-assigned organization identifier for a user's organization.
        :type org_id: str
        :param domain: The domain name to be verified.
        :type domain: str
        :param claim_domain: A boolean to specify whether the domain needs to be claimed. The default value is false.
            If false, the domain will be verified but not claimed.
        :type claim_domain: bool
        :param reserve_domain: For FedRAMP only: If true, add the domain to the FedRAMP reserved domain list. The
            default value is false.
        :type reserve_domain: bool
        :rtype: :class:`DomainVerification`
        """
        body: dict[str, Any] = dict()
        body['domain'] = domain
        if claim_domain is not None:
            body['claimDomain'] = claim_domain
        if reserve_domain is not None:
            body['reserveDomain'] = reserve_domain
        url = self.ep(f'{org_id}/actions/verifyDomain')
        data = super().post(url, json=body)
        r = DomainVerification.model_validate(data)
        return r
