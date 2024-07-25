import json
import os.path

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.telephony.devices import DeleteImageRequestObject


class TestBackgroundImages(TestCaseWithLog):

    def test_list(self):
        """
        list all background images
        """
        images = self.api.telephony.devices.list_background_images()
        print(f'got {len(images.background_images)} images')

    def test_upload(self):
        """
        upload a background image
        """
        bg_image = os.path.abspath('./sonda.png')
        devices = list(self.api.devices.list(product_type='phone', product='Cisco 8851'))
        target_device = next((d for d in devices if 'Henry Green' in d.display_name), None)
        dapi = self.api.telephony.devices
        images = dapi.list_background_images()
        names = set(im.file_name for im in images.background_images)
        new_name = next(name
                        for i in range(1, 100)
                        if (name := f'test_{i:02}.png') not in names)
        result = self.api.telephony.devices.upload_background_image(device_id=target_device.device_id, file=bg_image,
                                                                    file_name=new_name)
        print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        images = dapi.list_background_images()
        print(json.dumps(images.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

    @async_test
    async def test_as_upload(self):
        """
        upload a background image (async)
        """
        bg_image = os.path.abspath('./sonda.png')
        devices = list(self.api.devices.list(product_type='phone', product='Cisco 8851'))
        target_device = next((d for d in devices if 'Henry Green' in d.display_name), None)
        dapi = self.api.telephony.devices
        images = dapi.list_background_images()
        names = set(im.file_name for im in images.background_images)
        new_name = next(name
                        for i in range(1, 100)
                        if (name := f'test_{i:02}.png') not in names)
        result = await self.async_api.telephony.devices.upload_background_image(device_id=target_device.device_id,
                                                                                file=bg_image,
                                                                                file_name=new_name)
        print(json.dumps(result.model_dump(mode='json', by_alias=True), indent=2))

    def test_delete_all(self):
        """
        Delete all background images
        """
        dapi = self.api.telephony.devices
        images = dapi.list_background_images()
        requests = [DeleteImageRequestObject(file_name=im.file_name, force_delete=True)
                    for im in images.background_images]
        if not requests:
            self.skipTest('No background images to delete')
        r = dapi.delete_background_images(requests)
        self.assertEqual(0, r.count)
        self.assertTrue(all(i.result.status == 200 for i in r.items))
