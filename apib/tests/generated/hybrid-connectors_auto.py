from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Alarm', 'AlarmCollection', 'AlarmSeverity', 'Connector', 'ConnectorCollection', 'ConnectorStatus', 'ConnectorType']


class ConnectorStatus(str, Enum):
    #: Indicates that the connector is working as it should.
    operational = 'operational'
    #: Indicates that the connector has problems with one or more dependent components.
    impaired = 'impaired'
    #: Indicates that the connector is completely non-functional.
    outage = 'outage'
    #: Reports the current maintenance mode state of the connector.
    maintenancemode = 'maintenanceMode'


class ConnectorType(str, Enum):
    expresswaymanagement = 'expresswayManagement'
    calendar = 'calendar'
    call = 'call'
    message = 'message'
    expresswayserviceability = 'expresswayServiceability'
    ecpserviceability = 'ecpServiceability'
    videomesh = 'videoMesh'
    datasecurity = 'dataSecurity'
    care = 'care'
    caremanagement = 'careManagement'


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
    #: - `critical`
    #: - `error`
    #: - `warning`
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
    hybridConnectorId: Optional[str] = None


class Connector(ApiModel):
    #: A unique identifier for the connector.
    #: example: Y2lZY76123
    id: Optional[str] = None
    #: The ID of the organization to which this hybrid connector belongs.
    #: example: Y2lzY29zcGFyazovL3
    orgId: Optional[str] = None
    #: The ID of the cluster this connector belongs to.
    #: example: Y2lZY76123abbb
    hybridClusterId: Optional[str] = None
    #: The hostname of the system the connector is running on.
    #: example: foo.example.org
    hostname: Optional[str] = None
    #: The status of the connector:
    #: - `operational` indicates that the connector is working as it should.
    #: - `impaired` indicates that the connector has problems with one or more dependent components.
    #: - `outage` indicates that the connector is completely non-functional.
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


class ConnectorCollection(ApiModel):
    #: An array of hybrid connector objects.
    items: Optional[list[Connector]] = None


class AlarmCollection(ApiModel):
    items: Optional[list[Alarm]] = None
