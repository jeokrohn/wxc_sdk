"""
Call intercept API
"""
import os
from io import BufferedReader
from typing import Optional, Union

from pydantic import Field
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum
from ..common import Greeting

__all__ = ['InterceptTypeIncoming', 'InterceptNumber', 'InterceptAnnouncements', 'InterceptSettingIncoming',
           'InterceptTypeOutgoing', 'InterceptSettingOutgoing', 'InterceptSetting', 'CallInterceptApi']


class InterceptTypeIncoming(str, Enum):
    #: incoming calls are intercepted. Incoming calls are routed as destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class InterceptNumber(ApiModel):
    """
    Information about a number announcement.
    """
    #: If true, the caller will hear this number when the call is intercepted.
    enabled: Optional[bool] = None
    #: number caller will hear announced.
    destination: Optional[str] = None


class InterceptAnnouncements(ApiModel):
    """
    Settings related to how incoming calls are handled when the intercept feature is enabled.
    """
    greeting: Optional[Greeting] = None
    #: Filename of custom greeting, will be an empty string if no custom greeting has been uploaded.
    file_name: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumber] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumber] = None

    @staticmethod
    def default() -> 'InterceptAnnouncements':
        """
        Default for incoming call intercept announcement settings
        """
        return InterceptAnnouncements(greeting=Greeting.default, new_number=InterceptNumber(enabled=False),
                                      zero_transfer=InterceptNumber(enabled=False))


class InterceptSettingIncoming(ApiModel):
    """
    Settings related to how incoming calls are handled when the intercept feature is enabled.
    """
    intercept_type: Optional[InterceptTypeIncoming] = Field(alias='type', default=None)
    #: If true, the destination will be the person's voicemail.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncements] = None

    @staticmethod
    def default() -> 'InterceptSettingIncoming':
        """
        Default incoming call intercept settings
        """
        return InterceptSettingIncoming(intercept_type=InterceptTypeIncoming.intercept_all, voicemail_enabled=False,
                                        announcements=InterceptAnnouncements.default())


class InterceptTypeOutgoing(str, Enum):
    #: Outgoing calls are routed as destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class InterceptSettingOutgoing(ApiModel):
    intercept_type: Optional[InterceptTypeOutgoing] = Field(alias='type', default=None)
    #: If true, when the person attempts to make an outbound call, a system default message is played and the call is
    #: made to the destination phone number
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    destination: Optional[str] = None

    @staticmethod
    def default() -> 'InterceptSettingOutgoing':
        """
        Default outgoing call intercept settings
        """
        return InterceptSettingOutgoing(intercept_type=InterceptTypeOutgoing.intercept_all, transfer_enabled=False)


class InterceptSetting(ApiModel):
    """
    A person's call intercept settings
    """
    #: true if call intercept is enabled.
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptSettingIncoming] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[InterceptSettingOutgoing] = None

    @staticmethod
    def default() -> 'InterceptSetting':
        """
        Default call intercept settings.
        """
        return InterceptSetting(enabled=False,
                                incoming=InterceptSettingIncoming.default(),
                                outgoing=InterceptSettingOutgoing.default())

    def update(self) -> dict:
        """
        data for update

        :meta private:
        """
        return self.model_dump(mode='json', exclude_none=True, by_alias=True,
                               exclude={'incoming': {'announcements': 'file_name'}})


class CallInterceptApi(PersonSettingsApiChild):
    """
    API for call intercept settings

    Also used for virtual lines and workspaces
    """

    feature = 'intercept'

    def read(self, entity_id: str, org_id: str = None) -> InterceptSetting:
        """
        Read Call Intercept Settings

        Retrieves Call Intercept Settings

        The intercept feature gracefully takes an entity’s phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none,
        some, or all incoming calls to the specified entity are intercepted. Also depending on the service
        configuration, outgoing calls are intercepted or rerouted to another location.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's call intercept settings
        :rtype: InterceptSetting
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        return InterceptSetting.model_validate(self.get(ep, params=params))

    def configure(self, entity_id: str, intercept: InterceptSetting, org_id: str = None):
        """
        Configure Call Intercept Settings

        Configures Call Intercept Settings

        The intercept feature gracefully takes an entity’s phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified entity are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param intercept: new intercept settings
        :type intercept: InterceptSetting
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        data = intercept.update()
        self.put(ep, params=params, json=data)

    def greeting(self, entity_id: str, content: Union[BufferedReader, str],
                 upload_as: str = None, org_id: str = None):
        """
        Configure Call Intercept Greeting

        ConfigureCall Intercept Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by an entity to update their settings.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        if isinstance(content, str):
            upload_as = os.path.basename(content)
            content = open(content, mode='rb')
            must_close = True
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder({'file': (upload_as, content, 'audio/wav')})
        ep = self.f_ep(person_id=entity_id, path='actions/announcementUpload/invoke')
        params = org_id and {'orgId': org_id} or None
        try:
            self.post(ep, data=encoder, headers={'Content-Type': encoder.content_type},
                      params=params)
        finally:
            if must_close:
                content.close()
        return
