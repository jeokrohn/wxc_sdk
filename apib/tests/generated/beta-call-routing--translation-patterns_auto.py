from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaCallRoutingWithTranslationPatternsApi', 'Location', 'TranslationPatternGet', 'TranslationPatternItem']


class Location(ApiModel):
    #: Location name associated with the translation pattern.
    #: example: Site 1
    name: Optional[str] = None
    #: Location identifier associated with the translation pattern.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2M5YTVhYzNjLTQyZDMtNDI3NC04OWFkLTc5NjYxNjc1YTQwNA
    id: Optional[str] = None


class TranslationPatternItem(ApiModel):
    #: Unique identifier for a translation pattern.
    #: example: Y2lzY29zcGFyazovL3VzL0RJR0lUX1BBVFRFUk5TLzg3NGRjMjM1LTgwNTktNGM4OC05ZjU5LTRiNjdkZDJhZTZjMg
    id: Optional[str] = None
    #: Name given to a translation pattern for an organization.
    #: example: CHNHelpDesk
    name: Optional[str] = None
    #: Matching pattern given to a translation pattern for an organization.
    #: example: +91[2-7]XX21
    matching_pattern: Optional[str] = None
    #: Replacement pattern given to a translation pattern for an organization.
    #: example: +91352133
    replacement_pattern: Optional[str] = None
    #: Level at which the translation pattern is created. The level can either be `Organization` or `Location`.
    #: example: Location
    level: Optional[str] = None
    #: Location details for the translation pattern when the level is `Location`.
    location: Optional[Location] = None


class TranslationPatternGet(ApiModel):
    #: Unique identifier for a translation pattern.
    #: example: Y2lzY29zcGFyazovL3VzL0RJR0lUX1BBVFRFUk5TLzg3NGRjMjM1LTgwNTktNGM4OC05ZjU5LTRiNjdkZDJhZTZjMg
    id: Optional[str] = None
    #: Name given to a translation pattern for an organization.
    #: example: CHNHelpDesk
    name: Optional[str] = None
    #: Matching pattern given to a translation pattern for an organization.
    #: example: +91[2-7]XX21
    matching_pattern: Optional[str] = None
    #: Replacement pattern given to a translation pattern for an organization.
    #: example: +91352133
    replacement_pattern: Optional[str] = None


class BetaCallRoutingWithTranslationPatternsApi(ApiChild, base='telephony/config/callRouting/translationPatterns'):
    """
    Beta Call Routing with Translation Patterns
    
    A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls only.
    
    Call routing supports translation patterns at the organization level.
    
    Viewing these translation patterns for an organization requires a full or read-only administrator auth token with a
    scope of `spark-admin:telephony_config_read`.
    
    Modifying these translation patterns for an organization requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def create_a_translation_pattern_for_an_organization(self, name: str, matching_pattern: str,
                                                         replacement_pattern: str, org_id: str = None) -> str:
        """
        Create a Translation Pattern for an Organization

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Create a translation pattern for a given organization.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param name: Name given to a translation pattern for an organization.
        :type name: str
        :param matching_pattern: Matching pattern given to a translation pattern for an organization.
        :type matching_pattern: str
        :param replacement_pattern: Replacement pattern given to a translation pattern for an organization.
        :type replacement_pattern: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['matchingPattern'] = matching_pattern
        body['replacementPattern'] = replacement_pattern
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def retrieve_a_list_of_translation_patterns(self, limit_to_location_id: str = None,
                                                limit_to_org_level_enabled: str = None, name: str = None,
                                                matching_pattern: str = None, org_id: str = None,
                                                **params) -> Generator[TranslationPatternItem, None, None]:
        """
        Retrieve a list of Translation Patterns

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Retrieve a list of translation patterns for a given organization.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param limit_to_location_id: When a location ID is passed, then return only the corresponding location level
            translation patterns.
        :type limit_to_location_id: str
        :param limit_to_org_level_enabled: When set to be `true`, then return only the organization-level translation
            patterns.
        :type limit_to_org_level_enabled: str
        :param name: Only return translation patterns with the matching `name`.
        :type name: str
        :param matching_pattern: Only return translation patterns with the matching `matchingPattern`.
        :type matching_pattern: str
        :param org_id: ID of the organization containing the translation patterns.
        :type org_id: str
        :return: Generator yielding :class:`TranslationPatternItem` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if limit_to_location_id is not None:
            params['limitToLocationId'] = limit_to_location_id
        if limit_to_org_level_enabled is not None:
            params['limitToOrgLevelEnabled'] = limit_to_org_level_enabled
        if name is not None:
            params['name'] = name
        if matching_pattern is not None:
            params['matchingPattern'] = matching_pattern
        url = self.ep()
        return self.session.follow_pagination(url=url, model=TranslationPatternItem, item_key='translationPatterns', params=params)

    def retrieve_the_details_of_a_translation_pattern_for_an_organization(self, translation_id: str,
                                                                          org_id: str = None) -> TranslationPatternGet:
        """
        Retrieve the details of a Translation Pattern for an Organization

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Retrieve the details of a translation pattern for a given organization.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param translation_id: Retrieve the translation pattern with the matching ID.
        :type translation_id: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: :class:`TranslationPatternGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{translation_id}')
        data = super().get(url, params=params)
        r = TranslationPatternGet.model_validate(data)
        return r

    def modify_a_translation_pattern_for_an_organization(self, translation_id: str, name: str = None,
                                                         matching_pattern: str = None,
                                                         replacement_pattern: str = None, org_id: str = None):
        """
        Modify a Translation Pattern for an Organization

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Modify a translation pattern for a given organization.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param translation_id: Modify translation pattern with the matching ID.
        :type translation_id: str
        :param name: Name given to a translation pattern for an organization.
        :type name: str
        :param matching_pattern: Matching pattern given to a translation pattern for an organization.
        :type matching_pattern: str
        :param replacement_pattern: Replacement pattern given to a translation pattern for an organization.
        :type replacement_pattern: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if matching_pattern is not None:
            body['matchingPattern'] = matching_pattern
        if replacement_pattern is not None:
            body['replacementPattern'] = replacement_pattern
        url = self.ep(f'{translation_id}')
        super().put(url, params=params, json=body)

    def delete_a_translation_pattern(self, translation_id: str, org_id: str = None):
        """
        Delete a Translation Pattern

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Delete a translation pattern for a given organization.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param translation_id: Delete a translation pattern with the matching ID.
        :type translation_id: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{translation_id}')
        super().delete(url, params=params)
