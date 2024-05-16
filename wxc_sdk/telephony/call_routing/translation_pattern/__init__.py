from collections.abc import Generator
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['TranslationPatternsApi', 'TranslationPattern']


class TranslationPattern(ApiModel):
    #: Unique identifier for a translation pattern.
    id: Optional[str] = None
    #: Name given to a translation pattern for an organization.
    name: Optional[str] = None
    #: Matching pattern given to a translation pattern for an organization.
    matching_pattern: Optional[str] = None
    #: Replacement pattern given to a translation pattern for an organization.
    replacement_pattern: Optional[str] = None

    def create_update(self) -> dict:
        """
        Date for create() and update()

        :meta private:
        """
        return self.model_dump(mode='json', exclude={'id'}, by_alias=True)


class TranslationPatternsApi(ApiChild, base='telephony/config/callRouting/translationPatterns'):
    """
    Translation Patterns

    A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls only.

    Call routing supports translation patterns at the organization level.

    Viewing these translation patterns for an organization requires a full or read-only administrator auth token with a
    scope of `spark-admin:telephony_config_read`.

    Modifying these translation patterns for an organization requires a full administrator auth token with a scope
    of `spark-admin:telephony_config_write`.
    """

    def create(self, pattern: TranslationPattern,
               org_id: str = None) -> str:
        """
        Create a Translation Pattern

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Create a translation pattern for a given organization.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param pattern: Translation pattern to create
        :type pattern: TranslationPattern
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = pattern.create_update()
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def list(self, limit_to_location_id: str = None,
             limit_to_org_level_enabled: bool = None, name: str = None,
             matching_pattern: str = None, org_id: str = None,
             **params) -> Generator[TranslationPattern, None, None]:
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
        :type limit_to_org_level_enabled: bool
        :param name: Only return translation patterns with the matching `name`.
        :type name: str
        :param matching_pattern: Only return translation patterns with the matching `matchingPattern`.
        :type matching_pattern: str
        :param org_id: ID of the organization containing the translation patterns.
        :type org_id: str
        :return: Generator yielding :class:`TranslationPatternGet` instances
        """
        params = org_id and {'orgId': org_id} or None
        if limit_to_location_id is not None:
            params['limitToLocationId'] = limit_to_location_id
        if limit_to_org_level_enabled is not None:
            params['limitToOrgLevelEnabled'] = str(limit_to_org_level_enabled).lower()
        if name is not None:
            params['name'] = name
        if matching_pattern is not None:
            params['matchingPattern'] = matching_pattern
        url = self.ep()
        return self.session.follow_pagination(url=url, model=TranslationPattern, item_key='translationPatterns',
                                              params=params)

    def details(self, translation_id: str,
                org_id: str = None) -> TranslationPattern:
        """
        Retrieve the details of a Translation Pattern

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Retrieve the details of a translation pattern for a given organization.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param translation_id: Retrieve the translation pattern with the matching ID.
        :type translation_id: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: :class:`TranslationPattern`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{translation_id}')
        data = super().get(url, params=params)
        r = TranslationPattern.model_validate(data)
        return r

    def update(self, pattern: TranslationPattern, org_id: str = None):
        """
        Modify a Translation Pattern

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Modify a translation pattern for a given organization.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param pattern: Translation pattern to be updated
        :type pattern: TranslationPattern
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = pattern.create_update()
        url = self.ep(f'{pattern.id}')
        super().put(url, params=params, json=body)

    def delete(self, translation_id: str, org_id: str = None):
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
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{translation_id}')
        super().delete(url, params=params)
