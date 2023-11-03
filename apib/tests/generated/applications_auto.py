from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Application', 'ApplicationOrgSubmissionStatus', 'ApplicationSubmissionStatus', 'ApplicationType',
            'ApplicationsCollectionResponse', 'ListApplicationsOrderBy', 'ListApplicationsType']


class ApplicationType(str, Enum):
    integration = 'integration'


class ApplicationSubmissionStatus(str, Enum):
    none_ = 'none'
    submitted = 'submitted'
    in_review = 'in_review'
    pending_approval = 'pending_approval'
    approved = 'approved'


class ApplicationOrgSubmissionStatus(str, Enum):
    none_ = 'none'
    submitted = 'submitted'
    in_review = 'in_review'
    pending_approval = 'pending_approval'
    approved = 'approved'
    none_ = 'none'


class Application(ApiModel):
    #: A unique identifier for the application.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZg
    id: Optional[str] = None
    #: A descriptive name for the application.
    #: example: My Great App
    name: Optional[str] = None
    #: A unique URL-friendly identifier for the application.
    #: example: my-great-app-my-company
    friendly_id: Optional[str] = None
    #: The type of application.
    #: example: integration
    type: Optional[ApplicationType] = None
    #: URL for the application's logo.
    #: example: https://cdn.example.com/my-great-app-logo.png
    logo: Optional[str] = None
    #: Brief description of the application.
    #: example: My Great App helps you get things done.
    tagline: Optional[str] = None
    #: Description of the application.
    #: example: My Great App helps you achieve your business goals by getting out of the way and letting you focus on what's important. Use My Great App to unlock the potential of your business.
    description: Optional[str] = None
    #: URL for the application's first screenshot.
    #: example: https://cdn.example.com/my-great-app-screenshot-1.png
    screenshot1: Optional[str] = None
    #: URL for the application's second screenshot.
    #: example: https://cdn.example.com/my-great-app-screenshot-2.png
    screenshot2: Optional[str] = None
    #: URL for the application's third screenshot.
    #: example: https://cdn.example.com/my-great-app-screenshot-3.png
    screenshot3: Optional[str] = None
    #: An array of languages supported by the application.
    #: example: ['en-US', 'es-MX']
    supported_languages: Optional[list[str]] = None
    #: An array of categories the application belongs to.
    #: example: ['productivity', 'other']
    categories: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    #: URL for the application's informational video.
    #: example: https://youtu.be/abc123
    video_url: Optional[str] = None
    #: The ID of the organization to which this application belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: Contact email for the application.
    #: example: info@example.com
    contact_email: Optional[str] = None
    #: Contact name for the application.
    #: example: John Andersen
    contact_name: Optional[str] = None
    #: Company name for the application.
    #: example: Example, Inc.
    company_name: Optional[str] = None
    #: URL for the application's maintainer.
    #: example: https://www.example.com
    company_url: Optional[str] = None
    #: URL for the application's product information page.
    #: example: https://www.example.com/products/my-great-app
    product_url: Optional[str] = None
    #: URL for the application's support information.
    #: example: https://help.example.com/
    support_url: Optional[str] = None
    #: URL for the application's privacy policy.
    #: example: https://www.example.com/privacy-policy
    privacy_url: Optional[str] = None
    #: Oauth redirect URLs for the application (only present if the application is an integration).
    #: example: ['https://my-app.example.com/authenticate', 'https://my-app-staging.example.com/authenticate']
    redirect_urls: Optional[list[str]] = None
    #: Scopes requested by the application (only present if the application is an integration).
    #: example: ['spark:people_read', 'spark:messages_write']
    scopes: Optional[list[str]] = None
    #: An array of keywords associated with the application.
    #: example: ['productivity', 'efficiency']
    keywords: Optional[list[str]] = None
    #: The application's Oauth client ID.
    #: example: C1234567890ABCDEF
    client_id: Optional[str] = None
    #: If the application is a bot, this is the bot's email address. (only present if the application is a bot).
    #: example: my-great-app@webex.bot
    bot_email: Optional[str] = None
    #: If the application is a bot, this is the bot's personId (only present if the application is a bot).
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xMjM0NTY3OC05MGFiLWNkZWYtMTIzNC01Njc4OTBhYmNkZWY
    bot_person_id: Optional[str] = None
    #: Whether or not the application is featured on the Webex App Hub.
    is_featured: Optional[bool] = None
    #: Internal use only.
    is_native: Optional[bool] = None
    #: The date and time the application was submitted to Webex App Hub.
    #: example: 2017-12-01T07:00:00.000Z
    submission_date: Optional[datetime] = None
    #: The Webex App Hub submission status of the application.
    #: example: in_review
    submission_status: Optional[ApplicationSubmissionStatus] = None
    org_submission_status: Optional[ApplicationOrgSubmissionStatus] = None
    #: The ID of the person who created the application.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    created_by: Optional[str] = Field(alias='created_by', default=None)
    #: The date and time the application was created.
    #: example: 2017-10-01T07:00:00.000Z
    created: Optional[datetime] = None


class ApplicationsCollectionResponse(ApiModel):
    items: Optional[list[Application]] = None


class ListApplicationsType(str, Enum):
    integration = 'integration'
    bot = 'bot'


class ListApplicationsOrderBy(str, Enum):
    is_featured = 'isFeatured'
    last_submission_date = 'lastSubmissionDate'
    policy = 'policy'
    app_name = 'appName'
    name = 'name'
