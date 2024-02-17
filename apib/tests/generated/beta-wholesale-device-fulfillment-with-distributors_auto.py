from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaWholesaleDeviceFulfillmentWithDistributorsApi', 'CatalogResponse', 'CatalogResponseAvailability',
           'DistributorDetailsResponse', 'DistributorDetailsResponseCapabilities', 'DistributorResponse',
           'OrderRequestLineItem', 'OrderResponse', 'OrderResponseLineItem', 'OrderShippingDetails', 'Person']


class CatalogResponseAvailability(str, Enum):
    #: The catalog item is in stock and available to order.
    available = 'available'
    #: The catalog item is out of stock and not available to order.
    out_of_stock = 'out_of_stock'


class CatalogResponse(ApiModel):
    #: The catalog item ID.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0NBVEFMT0dJVEVNLzZmN2QzMTFjLTc1YjEtNGM4Ny04YTMyLTIwODMwNjcyYjE4Yg
    id: Optional[str] = None
    #: The catalog item SKU.
    #: example: CP-8845-k9=
    sku: Optional[str] = None
    #: The distributor ID.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RJU1RSSUJVVE9SL2MwNTYzN2U3LWE3MmYtNDcxZS05N2ZhLTVjNDM1MTRkODdkNA
    distributor_id: Optional[str] = None
    #: The catalog item product name.
    #: example: Cisco IP Phone 8845. Charcoal
    product_name: Optional[str] = None
    #: The availability of catalog item.
    #: example: available
    availability: Optional[CatalogResponseAvailability] = None
    #: The catalog item manufacturer name.
    #: example: Cisco
    manufacturer_name: Optional[str] = None


class DistributorDetailsResponseCapabilities(str, Enum):
    #: The distributor has the capability to create orders.
    create_order = 'create_order'
    #: The distributor has the capability to edit orders.
    edit_order = 'edit_order'
    #: The distributor has the capability to cancel orders.
    cancel_order = 'cancel_order'
    #: The distributor has the capability to retrieve orders.
    retrieve_order = 'retrieve_order'


class DistributorDetailsResponse(ApiModel):
    #: The distributor ID.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RJU1RSSUJVVE9SL2MwNTYzN2U3LWE3MmYtNDcxZS05N2ZhLTVjNDM1MTRkODdkNA
    id: Optional[str] = None
    #: The distributor name.
    #: example: Globex Corporation
    name: Optional[str] = None
    #: The distributor capabilities for device fulfillment orders.
    #: example: create_order
    capabilities: Optional[DistributorDetailsResponseCapabilities] = None


class DistributorResponse(ApiModel):
    #: The distributor name.
    #: example: Globex Corporation
    name: Optional[str] = None
    #: The distributor details url.
    #: example: https://webexapis.com/v1/wholesale/device/fulfillment/distributors/Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RJU1RSSUJVVE9SL2MwNTYzN2U3LWE3MmYtNDcxZS05N2ZhLTVjNDM1MTRkODdkNA
    url: Optional[str] = None


class OrderShippingDetails(ApiModel):
    #: The order recipient.
    #: example: David Forbes
    name: Optional[str] = None
    #: The order recipient's phone number.
    #: example: +1 468 23456789
    phone_number: Optional[str] = None
    #: The order recipient's email address.
    #: example: dforbes@test.com
    email: Optional[str] = None
    #: The order recipient's address line 1.
    #: example: Almond Telecom
    address_line1: Optional[str] = None
    #: The order recipient's address line 2.
    #: example: 45 North Glen Eagles Street
    address_line2: Optional[str] = None
    #: The order recipient's city.
    #: example: Springfield
    city: Optional[str] = None
    #: The order recipient's state.
    #: example: PA
    state: Optional[str] = None
    #: The order recipient's zip code.
    #: example: 19064
    zip_code: Optional[str] = None
    #: The order recipient's country.
    #: example: USA
    country: Optional[str] = None


class Person(ApiModel):
    #: The person ID which the line item is associated with.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wOTA5ODFhOS04Yjc1LTRkY2QtYWU4Zi1lZjQ3NjI3NDI4ZTQ
    id: Optional[str] = None
    #: The person display name for the line item.
    #: example: Dwight Schrute
    display_name: Optional[str] = None


class OrderResponseLineItem(ApiModel):
    #: The order line item number.
    #: example: 1
    line_item_number: Optional[str] = None
    #: The line item catalog identifier.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0NBVEFMT0dJVEVNLzZmN2QzMTFjLTc1YjEtNGM4Ny04YTMyLTIwODMwNjcyYjE4Yg
    catalog_id: Optional[str] = None
    #: The line item device display name.
    #: example: Cisco 8865
    display_name: Optional[str] = None
    #: The line item device SKU.
    #: example: CP-8865-K9=
    sku: Optional[str] = None
    #: The line item status.
    #: example: provisioned
    status: Optional[str] = None
    person: Optional[Person] = None
    workspace: Optional[Person] = None


class OrderResponse(ApiModel):
    #: A unique identifier for the order.
    #: example: '4560123456'
    order_number: Optional[str] = None
    #: The person ID used to place the order.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mZTc3NGJlLTFhNTUtNDM2NS05ODZhLWFiMzAyMThjYzVhYg
    ordered_by: Optional[str] = None
    #: The distributor ID
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RJU1RSSUJVVE9SL2MwNTYzN2U3LWE3MmYtNDcxZS05N2ZhLTVjNDM1MTRkODdkNA
    distributor_id: Optional[str] = None
    #: Descriptive name for the order.
    #: example: Almond Telecom Initial Cisco Device Order
    description: Optional[str] = None
    #: Tracking number for delivery, if available.
    tracking_number: Optional[str] = None
    #: A unique identifier for the customer.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The order delivery shipping details.
    shipping_details: Optional[OrderShippingDetails] = None
    #: The aggregated order status.
    #: example: Order Confirmed
    status: Optional[str] = None
    #: The date and time the order was created.
    #: example: 2022-11-15T10:14:44.712Z
    created: Optional[datetime] = None
    #: A list of order line items.
    line_items: Optional[list[OrderResponseLineItem]] = None


class OrderRequestLineItem(ApiModel):
    #: The line item catalog identifier.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0NBVEFMT0dJVEVNLzZmN2QzMTFjLTc1YjEtNGM4Ny04YTMyLTIwODMwNjcyYjE4Yg
    catalog_id: Optional[str] = None
    #: The person ID which the line item is associated with.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wOTA5ODFhOS04Yjc1LTRkY2QtYWU4Zi1lZjQ3NjI3NDI4ZTQ
    person_id: Optional[str] = None
    #: The workspace ID which the line item is associated with.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL1BMQUNFLzg2NDc2MmI4LTVlZGYtNDc0NC04ZWNmLTEyMjQ2OGIzMzFhMA
    workspace_id: Optional[str] = None


class BetaWholesaleDeviceFulfillmentWithDistributorsApi(ApiChild, base='wholesale/deviceFulfillment'):
    """
    Beta Wholesale Device Fulfillment with Distributors
    
    """

    def list_wholesale_device_catalog(self, distributor_id: str = None, product_name: str = None, sku: str = None,
                                      **params) -> Generator[CatalogResponse, None, None]:
        """
        List Wholesale Device Catalog

        List the device fulfillment catalog items associated with a Service Provider. There are a number of filter
        options, which can be combined in a single request.

        :param distributor_id: The distributor ID.
        :type distributor_id: str
        :param product_name: The device product name.
        :type product_name: str
        :param sku: The device SKU.
        :type sku: str
        :return: Generator yielding :class:`CatalogResponse` instances
        """
        if distributor_id is not None:
            params['distributorId'] = distributor_id
        if product_name is not None:
            params['productName'] = product_name
        if sku is not None:
            params['sku'] = sku
        url = self.ep('deviceCatalog')
        return self.session.follow_pagination(url=url, model=CatalogResponse, item_key='items', params=params)

    def get_wholesale_device_catalog_details(self, catalog_id: str) -> CatalogResponse:
        """
        Get Wholesale Device Catalog Details

        Retrieve details of a Wholesale device fulfillment catalog item.

        :param catalog_id: A unique identifier for the device fulfillment catalog item.
        :type catalog_id: str
        :rtype: :class:`CatalogResponse`
        """
        url = self.ep(f'deviceCatalog/{catalog_id}')
        data = super().get(url)
        r = CatalogResponse.model_validate(data)
        return r

    def list_wholesale_device_distributors(self) -> list[DistributorResponse]:
        """
        List Wholesale Device Distributors

        List the device fulfillment distributors associated with a Service Provider.

        :rtype: list[DistributorResponse]
        """
        url = self.ep('distributors')
        data = super().get(url)
        r = TypeAdapter(list[DistributorResponse]).validate_python(data['items'])
        return r

    def get_wholesale_device_distributor_details(self, distributor_id: str) -> DistributorDetailsResponse:
        """
        Get Wholesale Device Distributor Details

        Retrieve distributor information.

        :param distributor_id: The distributor ID.
        :type distributor_id: str
        :rtype: :class:`DistributorDetailsResponse`
        """
        url = self.ep(f'distributors/{distributor_id}')
        data = super().get(url)
        r = DistributorDetailsResponse.model_validate(data)
        return r

    def list_wholesale_device_orders(self, status: str = None, org_id: str = None,
                                     **params) -> Generator[OrderResponse, None, None]:
        """
        List Wholesale Device Orders

        List the device fulfillment orders associated with a Service Provider. There are a number of filter options,
        which can be combined in a single request.

        :param status: The aggregated order status.
        :type status: str
        :param org_id: Wholesale customer ID.
        :type org_id: str
        :return: Generator yielding :class:`OrderResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if status is not None:
            params['status'] = status
        url = self.ep('orders')
        return self.session.follow_pagination(url=url, model=OrderResponse, item_key='items', params=params)

    def create_a_wholesale_device_order(self, description: str, org_id: str, shipping_details: OrderShippingDetails,
                                        line_items: list[OrderRequestLineItem] = None) -> OrderResponse:
        """
        Create a Wholesale Device Order

        Create a Wholesale device fulfillment order.

        :param description: Description of the order.
        :type description: str
        :param org_id: A unique identifier for the customer.
        :type org_id: str
        :param shipping_details: The order delivery shipping details.
        :type shipping_details: OrderShippingDetails
        :param line_items: A list of order line items.
        :type line_items: list[OrderRequestLineItem]
        :rtype: :class:`OrderResponse`
        """
        body = dict()
        body['description'] = description
        body['orgId'] = org_id
        body['shippingDetails'] = loads(shipping_details.model_dump_json())
        if line_items is not None:
            body['lineItems'] = loads(TypeAdapter(list[OrderRequestLineItem]).dump_json(line_items, by_alias=True, exclude_none=True))
        url = self.ep('orders')
        data = super().post(url, json=body)
        r = OrderResponse.model_validate(data)
        return r

    def cancel_a_wholesale_device_order(self, order_number: str):
        """
        Cancel a Wholesale Device Order

        Cancel a Wholesale device fulfillment order.

        :param order_number: A unique identifier for the device fulfillment order.
        :type order_number: str
        :rtype: None
        """
        url = self.ep(f'orders/{order_number}')
        super().delete(url)

    def get_a_wholesale_device_order(self, order_number: str) -> OrderResponse:
        """
        Get a Wholesale Device Order

        Retrieve details of a Wholesale device fulfillment order.

        :param order_number: A unique identifier for the device fulfillment order.
        :type order_number: str
        :rtype: :class:`OrderResponse`
        """
        url = self.ep(f'orders/{order_number}')
        data = super().get(url)
        r = OrderResponse.model_validate(data)
        return r
