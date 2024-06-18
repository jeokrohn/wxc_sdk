from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaLocationCallRoutingWithTranslationPatternsApi', 'TranslationPatternGet']


class TranslationPatternGet(ApiModel):
    #: Unique identifier for a translation pattern.
    #: example: Y2lzY29zcGFyazovL3VzL0RJR0lUX1BBVFRFUk5TLzg3NGRjMjM1LTgwNTktNGM4OC05ZjU5LTRiNjdkZDJhZTZjMg
    id: Optional[str] = None
    #: A name given to a translation pattern for a location.
    #: example: CHNHelpDesk
    name: Optional[str] = None
    #: A matching pattern given to a translation pattern for a location.
    #: example: +91[2-7]XX21
    matching_pattern: Optional[str] = None
    #: A replacement pattern given to a translation pattern for a location.
    #: example: +91352133
    replacement_pattern: Optional[str] = None


class BetaLocationCallRoutingWithTranslationPatternsApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Location Call Routing with Translation Patterns
    
    A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls only.
    
    Call routing supports translation patterns at the location level.
    
    Viewing the translation pattern for a location requires a full or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`.
    
    Modifying a translation pattern for a location requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def create_a_translation_pattern_for_a_location(self, location_id: str, name: str, matching_pattern: str,
                                                    replacement_pattern: str, org_id: str = None) -> str:
        """
        Create a Translation Pattern for a Location

        Create a translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param name: A name given to a translation pattern for a location.
        :type name: str
        :param matching_pattern: A matching pattern given to a translation pattern for a location.
        :type matching_pattern: str
        :param replacement_pattern: A replacement pattern given to a translation pattern for a location.
        :type replacement_pattern: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
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
        url = self.ep(f'{location_id}/callRouting/translationPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def retrieve_a_specific_translation_pattern_for_a_location(self, location_id: str, translation_id: str,
                                                               org_id: str = None) -> TranslationPatternGet:
        """
        Retrieve a specific Translation Pattern for a Location

        Retrieve a specific translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param translation_id: Unique identifier for the translation pattern.
        :type translation_id: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: :class:`TranslationPatternGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/callRouting/translationPatterns/{translation_id}')
        data = super().get(url, params=params)
        r = TranslationPatternGet.model_validate(data)
        return r

    def modify_a_specific_translation_pattern_for_a_location(self, location_id: str, translation_id: str,
                                                             name: str = None, matching_pattern: str = None,
                                                             replacement_pattern: str = None, org_id: str = None):
        """
        Modify a specific Translation Pattern for a Location

        Modify a specific translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param translation_id: Unique identifier for the translation pattern.
        :type translation_id: str
        :param name: A name given to a translation pattern for a location.
        :type name: str
        :param matching_pattern: A matching pattern given to a translation pattern for a location.
        :type matching_pattern: str
        :param replacement_pattern: A replacement pattern given to a translation pattern for a location.
        :type replacement_pattern: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
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
        url = self.ep(f'{location_id}/callRouting/translationPatterns/{translation_id}')
        super().put(url, params=params, json=body)

    def delete_a_specific_translation_pattern_for_a_location(self, location_id: str, translation_id: str,
                                                             org_id: str = None):
        """
        Delete a specific Translation Pattern for a Location

        Delete a specific translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param translation_id: Unique identifier for the translation pattern.
        :type translation_id: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/callRouting/translationPatterns/{translation_id}')
        super().delete(url, params=params)
