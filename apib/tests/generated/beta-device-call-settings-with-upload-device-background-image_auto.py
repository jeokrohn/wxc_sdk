from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaDeviceCallSettingsWithUploadDeviceBackgroundImageApi', 'DeleteDeviceBackgroundImagesResponse',
           'DeleteImageRequestObject', 'DeleteImageResponseSuccessObject', 'DeleteImageResponseSuccessObjectResult',
           'ListBackgroundImagesObject', 'ReadTheListOfBackgroundImagesResponse',
           'UploadADeviceBackgroundImageResponse']


class ListBackgroundImagesObject(ApiModel):
    #: The URL of the image file.
    #: example: "/dms/Cisco_Phone_Background/background001"
    background_image_url: Optional[str] = None
    #: The name of the image file.
    #: example: CompanyLogoBlue
    file_name: Optional[str] = None


class DeleteImageResponseSuccessObjectResult(ApiModel):
    #: The status of the deletion.
    #: example: 200
    status: Optional[int] = None


class DeleteImageResponseSuccessObject(ApiModel):
    #: The name of the image file.
    #: example: CompanyLogoBlue
    file_name: Optional[str] = None
    #: The result of the deletion.
    result: Optional[DeleteImageResponseSuccessObjectResult] = None


class DeleteImageRequestObject(ApiModel):
    #: The name of the image file to be deleted.
    #: example: CompanyLogoBlue
    file_name: Optional[str] = None
    #: Flag to force delete the image. When `forceDelete` = true, if any device, location, or org level custom
    #: background URL is configured with the `backgroundImageURL` containing the filename being deleted, the
    #: background image is set to `None`.
    #: example: True
    force_delete: Optional[bool] = None


class ReadTheListOfBackgroundImagesResponse(ApiModel):
    #: Array of background images.
    background_images: Optional[list[ListBackgroundImagesObject]] = None
    #: The total number of images in the org.
    #: example: 2
    count: Optional[str] = None


class UploadADeviceBackgroundImageResponse(ApiModel):
    #: The name of the uploaded image file.
    #: example: CompanyLogoBlue
    filename: Optional[str] = None
    #: The URL of the uploaded image file.
    #: example: "/dms/Cisco_Phone_Background/background001"
    background_image_url: Optional[str] = None
    #: The total number of images in the org after uploading.
    #: example: 2
    count: Optional[str] = None


class DeleteDeviceBackgroundImagesResponse(ApiModel):
    #: Array of deleted images.
    items: Optional[list[DeleteImageResponseSuccessObject]] = None
    #: The total number of images in the org after deletion.
    #: example: 2
    count: Optional[str] = None


class BetaDeviceCallSettingsWithUploadDeviceBackgroundImageApi(ApiChild, base='telephony/config/devices'):
    """
    Beta Device Call Settings with Upload Device Background Image
    
    These APIs manage Webex Calling settings for Webex Calling devices.
    
    Viewing these read-only device settings requires a full, device, or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def read_the_list_of_background_images(self, org_id: str = None) -> ReadTheListOfBackgroundImagesResponse:
        """
        Read the List of Background Images

        Gets the list of device background images for an organization.

        Webex Calling supports the upload of up to 100 background image files for each org. These image files can then
        be referenced by MPP phones in that org for use as their background image.

        Retrieving this list requires a full, device, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieves the list of images in this organization.
        :type org_id: str
        :rtype: :class:`ReadTheListOfBackgroundImagesResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('backgroundImages')
        data = super().get(url, params=params)
        r = ReadTheListOfBackgroundImagesResponse.model_validate(data)
        return r

    def upload_a_device_background_image(self, device_id: str,
                                         org_id: str = None) -> UploadADeviceBackgroundImageResponse:
        """
        Upload a Device Background Image

        Configure a device's background image by uploading an image with file format, `.jpeg` or `.png`, encoded image
        file. Maximum image file size allowed to upload is 625 KB.

        The request must be a multipart/form-data request rather than JSON, using the image/jpeg or image/png
        content-type.

        Webex Calling supports the upload of up to 100 background image files for each org. These image files can then
        be referenced by MPP phones in that org for use as their background image.

        Uploading a device background image requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        multipart POST. This API can be utilized using other tools that support multipart POST, such as Postman.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Uploads the image in this organization.
        :type org_id: str
        :rtype: :class:`UploadADeviceBackgroundImageResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/actions/backgroundImageUpload/invoke')
        data = super().post(url, params=params)
        r = UploadADeviceBackgroundImageResponse.model_validate(data)
        return r

    def delete_device_background_images(self, background_images: list[DeleteImageRequestObject],
                                        org_id: str = None) -> DeleteDeviceBackgroundImagesResponse:
        """
        Delete Device Background Images

        Delete the list of designated device background images for an organization. Maximum is 10 images per request.

        Deleting a device background image requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param background_images: Array of images to be deleted.
        :type background_images: list[DeleteImageRequestObject]
        :param org_id: Deletes the list of images in this organization.
        :type org_id: str
        :rtype: :class:`DeleteDeviceBackgroundImagesResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['backgroundImages'] = TypeAdapter(list[DeleteImageRequestObject]).dump_python(background_images, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('backgroundImages')
        data = super().delete(url, params=params, json=body)
        r = DeleteDeviceBackgroundImagesResponse.model_validate(data)
        return r
