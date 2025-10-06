"""
app services settings API
"""
from dataclasses import dataclass
from typing import Optional

from . import AppSharedLineApi
from ..api_child import ApiChild
from ..base import ApiModel
from ..rest import RestSession

__all__ = ['AppServicesSettings', 'AppServicesApi']


class AppServicesSettings(ApiModel):
    """
    Person app services settings
    """
    #: When `true`, indicates to ring devices for outbound Click to Dial calls.
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for inbound Group Pages.
    ring_devices_for_group_page_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for Call Park recalled.
    ring_devices_for_call_park_enabled: Optional[bool] = None
    #: Indicates that the browser Webex Calling application is enabled for use.
    browser_client_enabled: Optional[bool] = None
    #: Device ID of WebRTC client. Returns only if `browserClientEnabled` is true.
    browser_client_id: Optional[str] = None
    #: Indicates that the desktop Webex Calling application is enabled for use.
    desktop_client_enabled: Optional[bool] = None
    #: Device ID of Desktop client. Returns only if `desktopClientEnabled` is true.
    desktop_client_id: Optional[str] = None
    #: Indicates that the tablet Webex Calling application is enabled for use.
    tablet_client_enabled: Optional[bool] = None
    #: Device ID of Tablet client. Returns only if `tabletClientEnabled` is true.
    tablet_client_id: Optional[str] = None
    #: Indicates that the mobile Webex Calling application is enabled for use.
    mobile_client_enabled: Optional[bool] = None
    #: Device ID of Mobile client. Returns only if `mobileClientEnabled` is true.
    mobile_client_id: Optional[str] = None
    #: Number of available device licenses for assigning devices/apps.
    available_line_count: Optional[int] = None

    def update(self) -> dict:
        """
        get dict for updates

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'browser_client_id', 'desktop_client_id',
                                        'tablet_client_id', 'mobile_client_id',
                                        'available_line_count'})


@dataclass(init=False, repr=False)
class AppServicesApi(ApiChild, base=''):
    """
    API for person's app services settings
    """

    shared_line: AppSharedLineApi

    def __init__(self, *, session: RestSession):
        """

        :meta private:
        """
        super().__init__(session=session)
        self.shared_line = AppSharedLineApi(session=session)

    def f_ep(self, person_id: str):
        """

        :meta private:
        """
        return self.ep(f'people/{person_id}/features/applications')

    def read(self, person_id: str, org_id: str = None) -> AppServicesSettings:
        """
        Retrieve a person's Application Services Settings New

        Gets mobile and PC applications settings for a user.

        Application services let you determine the ringing behavior for calls made to people in certain
        scenarios. You
        can also specify which devices can download the Webex Calling app.

        Requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`AppServicesSettings`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return AppServicesSettings.model_validate(data)

    def configure(self, person_id: str, settings: AppServicesSettings, org_id: str = None):
        """
        Modify a person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.

        This API requires a full or user administrator or location administrator auth token with the
        spark-admin:people_write scope.

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
        data = settings.update()
        self.put(ep, params=params, json=data)
