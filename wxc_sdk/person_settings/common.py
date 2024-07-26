from enum import Enum

from ..api_child import ApiChild
from ..rest import RestSession

__all__ = ['PersonSettingsApiChild', 'ApiSelector']


class ApiSelector(str, Enum):
    location = 'location'
    person = 'person'
    workspace = 'workspace'
    virtual_line = 'virtual_line'


class PersonSettingsApiChild(ApiChild, base=''):
    """
    Base class for all classes implementing person settings APIs
    """

    feature = None

    def __init__(self, *, session: RestSession, selector: ApiSelector = ApiSelector.person):
        # set parameters to get the correct URL templates
        #
        #               selector                    feature_prefix  url template
        # workspaces    workspaces                      /features/      workspaces/{person_id}/features/{feature}{path}
        # locations     telephony/config/locations      /               telephony/config/locations/{person_id}{path}
        # person        people                          /features       people/{person_id}/features/{feature}{path}
        # virtual line  telephony/config/virtualLines   /               telephony/config/virtualLines/{person_id}/{feature}
        self.feature_prefix = '/features/'
        if selector == ApiSelector.workspace:
            self.selector = 'workspaces'
        elif selector == ApiSelector.location:
            self.selector = 'telephony/config/locations'
            self.feature_prefix = '/'
        elif selector == ApiSelector.virtual_line:
            self.selector = 'telephony/config/virtualLines'
            self.feature_prefix = '/'
        elif selector == ApiSelector.person:
            self.selector = 'people'
        else:
            raise ValueError(f'Invalid selector: {selector}')
        super().__init__(session=session, base=self.selector)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(base='')
        if cls.feature is None:
            raise TypeError('feature has to be defined')

    def f_ep(self, person_id: str, path: str = None) -> str:
        """
        person specific feature endpoint like v1/people/{uid}/features/....

        :meta private:
        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param path: path in the endpoint after the feature base URL
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        # url templates:
        #
        #               selector                        feature_prefix  url template
        # workspaces    workspaces                      /features/      workspaces/{person_id}/features/{feature}{path}
        # locations     telephony/config/locations      /               telephony/config/locations/{person_id}{path}
        # person        people                          /features       people/{person_id}/features/{feature}{path}
        # virtual line  telephony/config/virtualLines   /               telephony/config/virtualLines/{person_id}/{feature}
        selector = self.selector
        feature_prefix = self.feature_prefix
        # some paths need to be remapped
        alternates = {
            ('workspaces', 'anonymousCallReject'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'bargeIn'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'callBridge'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'callPolicies'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'doNotDisturb'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'musicOnHold'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'outgoingPermission/digitPatterns'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'privacy'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'priorityAlert'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'pushToTalk'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'selectiveAccept'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'selectiveForward'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'selectiveReject'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'sequentialRing'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'simultaneousRing'): ('telephony/config/workspaces', '/'),
            ('workspaces', 'voicemail'): ('telephony/config/workspaces', '/'),
            ('people', 'agent'): ('telephony/config/people', '/'),
            ('people', 'callBridge'): ('telephony/config/people', '/features/'),
            ('people', 'outgoingPermission/'): ('telephony/config/people', '/'),
            ('people', 'outgoingPermission/accessCodes'): ('telephony/config/people', '/'),
            ('people', 'outgoingPermission/digitPatterns'): ('telephony/config/people', '/'),
            ('people', 'musicOnHold'): ('telephony/config/people', '/'),
        }
        if selector == 'people' and self.feature == 'voicemail' and path == '/passcode':
            # this is a new endpoint for users and is the only VM endpoint with a different URL structure
            return self.session.ep(f'telephony/config/people/{person_id}/voicemail/passcode')
        selector, feature_prefix = alternates.get((selector, self.feature), (selector, feature_prefix))
        return self.session.ep(f'{selector}/{person_id}{feature_prefix}{self.feature}{path}')
