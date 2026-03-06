import os
from io import BufferedReader
from typing import Union

from requests_toolbelt import MultipartEncoder

from wxc_sdk.api_child import ApiChild

__all__ = ['MeVoicemailApi']

from wxc_sdk.person_settings.voicemail import VoicemailSettings


class MeVoicemailApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> VoicemailSettings:
        """
        Read Voicemail Settings for a Person

        Retrieve a person's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_read`.

        :rtype: :class:`VoicemailSettings`
        """
        url = self.ep('settings/voicemail')
        data = super().get(url)
        r = VoicemailSettings.model_validate(data)
        return r

    def configure(self, settings: VoicemailSettings):
        """
        Configure Voicemail Settings for a Person

        Configure a person's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param settings: Voicemail settings
        :type settings: VoicemailSettings
        :rtype: None
        """
        body = settings.update()
        url = self.ep('settings/voicemail')
        super().put(url, json=body)

    def _configure_greeting(self, *, content: Union[BufferedReader, str],
                            upload_as: str = None,
                            greeting_key: str):
        """
        handle greeting upload

        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param greeting_key: 'busyGreetingUpload' or 'noAnswerGreetingUpload'
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
        url = self.ep(f'settings/voicemail/actions/{greeting_key}/invoke')
        try:
            self.post(url, data=encoder, headers={'Content-Type': encoder.content_type})
        finally:
            if must_close:
                content.close()

    def upload_busy_greeting(self, content: Union[BufferedReader, str],
                             upload_as: str = None):
        """
        Upload Voicemail Busy Greeting

        Uploads a new busy greeting audio file for the authenticated user's voicemail.

        This endpoint is part of the voicemail greeting management capabilities provided by the Webex Calling platform
        and is available when the `wxc-csg-hydra-call-184017-phase4` feature is enabled. The greeting must be in WAV
        format and not exceed 5000 kilobytes.

        Requires a user auth token with the `spark:telephony_config_write` scope. Only the authenticated user may
        upload greetings for their own voicemail.

        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :rtype: None
        """
        return self._configure_greeting(content=content, upload_as=upload_as,
                                        greeting_key='busyGreetingUpload')

    def upload_no_answer_greeting(self, content: Union[BufferedReader, str],
                                  upload_as: str = None):
        """
        Upload Voicemail No Answer Greeting

        Uploads a new no answer greeting audio file for the authenticated user's voicemail.

        This endpoint is part of the voicemail greeting management capabilities provided by the Webex Calling platform
        and is available when the `wxc-csg-hydra-call-184017-phase4` feature is enabled. The greeting must be in WAV
        format and not exceed 5000 kilobytes.

        Requires a user auth token with the `spark:telephony_config_write` scope. Only the authenticated user may
        upload greetings for their own voicemail.

        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :rtype: None
        """
        return self._configure_greeting(content=content, upload_as=upload_as,
                                        greeting_key='noAnswerGreetingUpload')
