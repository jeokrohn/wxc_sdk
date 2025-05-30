"""
app services settings API
"""
from typing import Optional

from .common import PersonSettingsApiChild
from ..base import ApiModel

__all__ = ['AppServicesSettings', 'AppServicesApi']


class AppServicesSettings(ApiModel):
    """
    Person app services settings
    """
    #: When true, indicates to ring devices for outbound Click to Dial calls.
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: When true, indicates to ring devices for inbound Group Pages.
    ring_devices_for_group_page_enabled: Optional[bool] = None
    #: When true, indicates to ring devices for Call Park recalled.
    ring_devices_for_call_park_enabled: Optional[bool] = None
    #: Indicates that the desktop Webex Calling application is enabled for use.
    desktop_client_enabled: Optional[bool] = None
    #: desktop client id
    desktop_client_id: Optional[str] = None
    #: Indicates that the tablet Webex Calling application is enabled for use.
    tablet_client_enabled: Optional[bool] = None
    tablet_client_id: Optional[str] = None
    #: indicates that the mobile Webex Calling application is enabled for use.
    mobile_client_enabled: Optional[bool] = None
    mobile_client_id: Optional[str] = None
    #: Number of available device licenses for assigning devices/apps.
    #: this value cannot be updated
    available_line_count: Optional[int] = None
    #: Indicates that the browser Webex Calling application is enabled for use.
    browser_client_enabled: Optional[bool] = None
    browser_client_id: Optional[str] = None


class AppServicesApi(PersonSettingsApiChild):
    """
    API for person's app services settings
    """

    feature = 'applications'

    def read(self, person_id: str, org_id: str = None) -> AppServicesSettings:
        """
        Retrieve a Person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to people in certain scenarios.
        You can also specify which devices can download the Webex Calling app.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: privacy settings
        :rtype: :class:`Privacy`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return AppServicesSettings.model_validate(data)

    def configure(self, person_id: str, settings: AppServicesSettings, org_id: str = None):
        """
        Modify a Person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`AppServicesSettings`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.model_dump_json(include={'ring_devices_for_click_to_dial_calls_enabled': True,
                                                 'ring_devices_for_group_page_enabled': True,
                                                 'ring_devices_for_call_park_enabled': True,
                                                 'desktop_client_enabled': True,
                                                 'tablet_client_enabled': True,
                                                 'mobile_client_enabled': True,
                                                 'browser_client_enabled': True})
        self.put(ep, params=params, data=data)
