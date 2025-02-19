import asyncio
import json
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.person_settings.personal_assistant import PersonalAssistant, PersonalAssistantPresence, \
    PersonalAssistantAlerting


class TestPersonalAssistant(TestCaseWithUsers):

    @async_test
    async def test_read_all(self):
        settings = await asyncio.gather(*[self.async_api.person_settings.personal_assistant.get(person_id=user.person_id)
                                    for user in self.users],
                                  return_exceptions=True)
        err =next((s for s in settings if isinstance(s, Exception)), None)
        if err:
            raise err
        print(f'Personal Assistant settings for {len(settings)} users')

    def test_set_end_date(self):
        """
        Try to update personal assistant settings for a random user
        """
        settings = PersonalAssistant(enabled=True, presence=PersonalAssistantPresence.out_of_office,
                                     until_date_time=datetime(year=2025,month=3, day=1, hour=0, minute=0, second=0,
                                                              tzinfo=ZoneInfo('Europe/Berlin')),
                                     transfer_enabled=True,
                                     transfer_number='+4961007739764',
                                     alerting=PersonalAssistantAlerting.alert_me_first,
                                     alert_me_first_number_of_rings=4)
        target = random.choice(self.users)
        print(f'Modifying settings for {target.display_name}')
        print(json.dumps(settings.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
        before = self.api.person_settings.personal_assistant.get(person_id=target.person_id)
        try:
            self.api.person_settings.personal_assistant.update(person_id=target.person_id, settings=settings)
            settings.until_date_time = settings.until_date_time.astimezone(ZoneInfo('UTC'))
            after = self.api.person_settings.personal_assistant.get(person_id=target.person_id)
            print(json.dumps(after.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
            after.until_date_time = after.until_date_time.astimezone(ZoneInfo('UTC'))
            after.transfer_number = after.transfer_number.replace('-','')
            self.assertEqual(settings, after)
        finally:
            # restore old settings
            before.transfer_number = before.transfer_number or None
            self.api.person_settings.personal_assistant.update(person_id=target.person_id, settings=before)

