from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Alarm', 'AlarmSeverity', 'Connector', 'ConnectorStatus', 'ConnectorType', 'HybridConnectorsApi']


class ConnectorStatus(str, Enum):
    #: Indicates that the connector is working as it should.
    operational = 'operational'
    #: Indicates that the connector has problems with one or more dependent components.
    impaired = 'impaired'
    #: Indicates that the connector is completely non-functional.
    outage = 'outage'
    #: Reports the current maintenance mode state of the connector.
    maintenance_mode = 'maintenanceMode'


class ConnectorType(str, Enum):
    expressway_management = 'expresswayManagement'
    calendar = 'calendar'
    call = 'call'
    message = 'message'
    expressway_serviceability = 'expresswayServiceability'
    ecp_serviceability = 'ecpServiceability'
    video_mesh = 'videoMesh'
    data_security = 'dataSecurity'
    care = 'care'
    care_management = 'careManagement'


class AlarmSeverity(str, Enum):
    critical = 'critical'
    warning = 'warning'
    alert = 'alert'
    error = 'error'


class Alarm(ApiModel):
    #: A unique identifier for the alarm.
    #: example: Y2lZY76123af234bbYY
    id: Optional[str] = None
    #: The date and time the alarm was raised.
    #: example: 2017-09-15T15:53:00Z
    created: Optional[datetime] = None
    #: The severity level of the alarm:
    #: 
    #: - `critical`
    #: 
    #: - `error`
    #: 
    #: - `warning`
    #: 
    #: - `alert`
    #: example: warning
    severity: Optional[AlarmSeverity] = None
    #: The title of the alarm.
    #: example: Something is wrong
    title: Optional[str] = None
    #: A description of the alarm.
    #: example: More detail about something being wrong
    description: Optional[str] = None
    #: The ID of the connector the alarm is raised on.
    #: example: Y2lZY76123af234bb
    hybrid_connector_id: Optional[str] = None


class Connector(ApiModel):
    #: A unique identifier for the connector.
    #: example: Y2lZY76123
    id: Optional[str] = None
    #: The ID of the organization to which this hybrid connector belongs.
    #: example: Y2lzY29zcGFyazovL3
    org_id: Optional[str] = None
    #: The ID of the cluster this connector belongs to.
    #: example: Y2lZY76123abbb
    hybrid_cluster_id: Optional[str] = None
    #: The hostname of the system the connector is running on.
    #: example: foo.example.org
    hostname: Optional[str] = None
    #: The status of the connector:
    #: 
    #: - `operational` indicates that the connector is working as it should.
    #: 
    #: - `impaired` indicates that the connector has problems with one or more dependent components.
    #: 
    #: - `outage` indicates that the connector is completely non-functional.
    #: 
    #: - `maintenanceMode` reports the current maintenance mode state of the connector.
    #: example: operational
    status: Optional[ConnectorStatus] = None
    #: The date and time the connector was created.
    #: example: 2017-09-15T15:53:00Z
    created: Optional[datetime] = None
    #: The type of connector.
    #: example: calendar
    type: Optional[ConnectorType] = None
    #: The version of the software installed.
    #: example: 1.9_foo_zz
    version: Optional[str] = None
    #: A list of alarms raised on the connector.
    alarms: Optional[list[Alarm]] = None


class HybridConnectorsApi(ApiChild, base='hybrid/connectors'):
    """
    Hybrid Connectors
    
    `Hybrid Connectors
    <https://www.cisco.com/c/en/us/solutions/collaboration/webex-hybrid-services/index.html>`_ are pieces of software that run on-premise and provide a link between the Webex Cloud and
    on-premise resources.
    
    For example, the Calendar Connector enables the linking of information from an on-premise Exchange server with the
    Webex Cloud. It allows, among other things, for the cloud to set up a Webex meeting when a user specifies `@webex`
    as the *Location* of a meeting in Outlook.
    
    Listing and viewing Hybrid Connectors requires an administrator auth token with the
    `spark-admin:hybrid_connectors_read` scope.
    
    Use this API to list the connectors configured in an organization and to determine if any connectors have any
    `unresolved alarms
    <https://help.webex.com/nuej5gfb/>`_ associated with them.
    """

    def list_hybrid_connectors(self, org_id: str = None) -> list[Connector]:
        """
        List Hybrid Connectors

        List hybrid connectors for an organization. If no `orgId` is specified, the default is the organization of the
        authenticated user.

        Only an admin auth token with the `spark-admin:hybrid_connectors_read` scope can list connectors.

        :param org_id: List hybrid connectors in this organization. If an organization is not specified, the
            organization of the caller will be used.
        :type org_id: str
        :rtype: list[Connector]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[Connector]).validate_python(data['items'])
        return r

    def get_hybrid_connector_details(self, connector_id: str) -> Connector:
        """
        Get Hybrid Connector Details

        Shows details for a hybrid connector, by ID.

        Only an admin auth token with the `spark-admin:hybrid_connectors_read` scope can see connector details.

        :param connector_id: The ID of the connector.
        :type connector_id: str
        :rtype: :class:`Connector`
        """
        url = self.ep(f'{connector_id}')
        data = super().get(url)
        r = Connector.model_validate(data)
        return r
