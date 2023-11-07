from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CatalogListResponse', 'CatalogResponse', 'CatalogResponseAvailability', 'DistributorDetailsResponse',
            'DistributorDetailsResponseCapabilities', 'DistributorListResponse', 'DistributorResponse',
            'OrderListResponse', 'OrderRequest', 'OrderRequestLineItem', 'OrderResponse', 'OrderResponseLineItem',
            'OrderShippingDetails', 'Person']


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


class CatalogListResponse(ApiModel):
    #: An array of Catalog Response objects.
    items: Optional[list[CatalogResponse]] = None


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


class DistributorListResponse(ApiModel):
    #: An array of Distributor Response objects.
    items: Optional[list[DistributorResponse]] = None


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
    line_item_number: Optional[datetime] = None
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


class OrderListResponse(ApiModel):
    #: An array of Order Response objects.
    items: Optional[list[OrderResponse]] = None


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


class OrderRequest(ApiModel):
    #: Description of the order.
    #: example: Almond Telecom Initial Cisco Device Order
    description: Optional[str] = None
    #: A unique identifier for the customer.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The order delivery shipping details.
    shipping_details: Optional[OrderShippingDetails] = None
    #: A list of order line items.
    line_items: Optional[list[OrderRequestLineItem]] = None


class BetaWholesaleDeviceFulfillmentWithDistributorsApi(ApiChild, base='wholesale/deviceFulfillment'):
    """
    Beta Wholesale Device Fulfillment with Distributors
    
    """
    ...