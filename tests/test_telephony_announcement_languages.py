from operator import attrgetter

from tests.base import TestCaseWithLog


class AnnouncementLanguages(TestCaseWithLog):
    def test_list_announcement_languages(self):
        """
        list announcement langauages
        """
        ann_languages = self.api.telephony.read_list_of_announcement_languages()
        ann_languages.sort(key=attrgetter('name'))
        name_len = max(map(len, map(attrgetter('name'), ann_languages)))
        print('\n'.join(f'{al.name:{name_len}} - {al.code}' for al in ann_languages))
