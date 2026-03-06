import asyncio
import json
from typing import List, Tuple, Union

from pydantic import TypeAdapter
from tests.base import TestWithRandomUserApi, async_test
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.me.mode_management import FeatureDetail


class TestMeModeManagement(TestWithRandomUserApi):
    # proxy = True

    @async_test
    async def test_get_features(self):
        """
        get mode management features for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.mode_management.get_features()
                    except AsRestError as e:
                        raise e
            # end of get_settings
            return

        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error mode management features for {user.display_name}: {result}")
            elif result is not None:
                result: List[List[ModeManagementFeature]]
                print(f"Mode management features for {user.display_name}: ")

                print(json.dumps(
                    TypeAdapter(List[List[ModeManagementFeature]]).dump_python(result, mode='json', exclude_unset=True,
                                                                               exclude_none=True),
                    indent=2))
        if err:
            raise err

    @async_test
    async def test_get_feature_details(self):
        """
        get mode management feature details for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    mm_api = as_api.me.mode_management
                    try:
                        features = await mm_api.get_features()
                        details = await asyncio.gather(*[mm_api.feature_get(f.id) for f in features],
                                                       return_exceptions=True)
                        return details
                    except Exception as e:
                        raise e
            # end of get_settings
            return

        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error mode management features for {user.display_name}: {result}")
            elif result is not None:
                result: List[FeatureDetail]
                print(f"Mode management features for {user.display_name}: ")

                print(json.dumps(
                    TypeAdapter(List[FeatureDetail]).dump_python(result, mode='json', exclude_unset=True,
                                                                 exclude_none=True),
                    indent=2))
        if err:
            raise err

    @async_test
    async def test_get_feature_details_and_modes(self):
        """
        get mode management feature details ana modes for all users
        """

        async def Nil():
            return None
        RTYPE = Tuple[ \
                List[Union[str, FeatureDetail]],
                List[Union[str, OperatingModeDetail]]]
        async def get_settings(user: Person) -> RTYPE:
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    mm_api = as_api.me.mode_management

                    async def get_modes(f: ModeManagementFeature, fd: FeatureDetail):
                        # get mode details for all modes of given feature
                        return await asyncio.gather(*[mm_api.get_operating_mode(feature_id=f.id, mode_id=mode.id)
                                                      for mode in fd.modes],
                                                    return_exceptions=True)

                    try:
                        features = await mm_api.get_features()
                        details = await asyncio.gather(*[mm_api.feature_get(f.id) for f in features],
                                                       return_exceptions=True)
                        tasks = []
                        for feature, feature_detail in zip(features, details):
                            if isinstance(feature_detail, Exception):
                                tasks.append(Nil())
                            else:
                                feature_detail: FeatureDetail
                                tasks.append(get_modes(feature, feature_detail))
                        modes = await asyncio.gather(*tasks, return_exceptions=True)
                        return details, modes
                    except Exception as e:
                        return f'{e}'
            # end of get_settings
            return

        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        print(json.dumps(TypeAdapter(RTYPE).dump_python(results, mode='json',
                                                        exclude_none=True, by_alias=True),
                         indent=2))
