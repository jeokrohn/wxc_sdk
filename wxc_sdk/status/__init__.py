"""
Webex Status API as described at https://status.webex.com/api
"""
from datetime import datetime
from typing import Optional

from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['Component', 'IncidentUpdate', 'Incident', 'WebexStatus', 'StatusSummary', 'StatusAPI']


class Component(ApiModel):
    updated_at: Optional[datetime] = None
    group_id: Optional[str] = None
    name: Optional[str] = None
    fedramp: Optional[bool] = Field(alias='fedRAMP')
    commercial: Optional[bool] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    id: Optional[str] = None
    position: Optional[int] = None
    product_group: Optional[str] = None
    status: Optional[str] = None
    is_group: Optional[bool] = None
    components: Optional[list[str]] = Field(default_factory=list)
    link: Optional[str] = None
    external_id: Optional[str] = None
    help_link: Optional[str] = Field(alias='helpLink')


class IncidentUpdate(ApiModel):
    incident_id: Optional[str] = None
    external_id: Optional[str] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    body: Optional[str] = None
    status: Optional[str] = None


class Incident(ApiModel):
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    impact: Optional[str] = None
    incident_type: Optional[str] = None
    fedramp: Optional[bool] = Field(alias='fedRAMP')
    commercial: Optional[bool] = None
    change: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    components: list[Component]
    incident_updates: list[IncidentUpdate]
    id: Optional[str] = None
    status: Optional[str] = None
    external_id: Optional[str] = None
    source_id: Optional[str] = None
    change_id: Optional[str] = None
    publication_id: Optional[str] = None
    incident_number: Optional[str] = None


class WebexStatus(ApiModel):
    indicator: Optional[str] = None


class StatusSummary(ApiModel):
    incidents: list[Incident]
    components: list[Component]
    scheduled_maintenances: list[Incident]
    status: WebexStatus


class StatusAPI(ApiChild, base='status'):
    """
    Webex Status API as described at https://status.webex.com/api
    """

    # noinspection PyMethodOverriding
    def ep(self, path: str):
        """

        :meta private:
        """
        return f'https://status.webex.com/{path}.json'

    def summary(self) -> StatusSummary:
        """
        Get a summary of the status page, including a status indicator, component statuses, unresolved incidents,
        and any upcoming or in-progress scheduled maintenances.

        :return: Status summary
        :rtype: StatusSummary
        """
        url = self.ep('index')
        data = self.session.rest_get(url=url)
        return StatusSummary.model_validate(data)

    def status(self) -> str:
        """
        Get the status rollup for the whole page. This response includes an indicator - one of green (operational),
        yellow (under_maintenance/degraded_performance/partial_outage), red (major_outage).

        :return: Webex status
        :rtype: str
        """
        url = self.ep('status')
        data = self.session.rest_get(url=url)
        return data['status']['indicator']

    def components(self) -> list[Component]:
        """
        Get the components for the status page. Each component is listed along with its status - one of operational,
        under_maintenance,degraded_performance, partial_outage, or major_outage.

        :return: list of components
        :rtype: list[Component]
        """
        url = self.ep('components')
        data = self.session.rest_get(url=url)
        return TypeAdapter(list[Component]).validate_python(data['components'])

    def unresolved_incidents(self) -> list[Incident]:
        """
        Get a list of any unresolved incidents. This response will only return incidents in the Investigating,
        Identified, or Monitoring state.

        :return: list of incidents
        :rtype: list[Incident]
        """
        url = self.ep('unresolved-incidents')
        data = self.session.rest_get(url=url)
        return TypeAdapter(list[Incident]).validate_python(data['incidents'])

    def all_incidents(self) -> list[Incident]:
        """
        Get a list of the 50 most recent incidents. This includes all unresolved incidents as described above,
        as well as those in the Resolved state.

        :return: list of incidents
        :rtype: list[Incident]
        """
        url = self.ep('all-incidents')
        data = self.session.rest_get(url=url)
        return TypeAdapter(list[Incident]).validate_python(data['incidents'])

    def upcoming_scheduled_maintenances(self) -> list[Incident]:
        """
        Scheduled maintenances are planned outages, upgrades, or general notices that you're working on
        infrastructure and disruptions may occurr. A close sibling of Incidents, each usually goes through a
        progression of statuses listed below, with an impact calculated from a blend of component statuses (or an
        optional override).

        Status: Scheduled, In Progress, or Completed

        Impact: Maintenance

        :return: list of incidents
        :rtype: list[Incident]
        """
        url = self.ep('upcoming-scheduled-maintenances')
        data = self.session.rest_get(url=url)
        return TypeAdapter(list[Incident]).validate_python(data['scheduled_maintenances'])

    def active_scheduled_maintenances(self) -> list[Incident]:
        """
        Get a list of any active maintenances. This response will only return scheduled maintenances in the In
        Progress state.

        :return: list of incidents
        :rtype: list[Incident]
        """
        url = self.ep('active-scheduled-maintenances')
        data = self.session.rest_get(url=url)
        return TypeAdapter(list[Incident]).validate_python(data['scheduled_maintenances'])

    def all_scheduled_maintenances(self) -> list[Incident]:
        """
        Get a list of the 50 most recent scheduled maintenances. This includes scheduled maintenances in Scheduled ,
        In Progress or Completed state.

        :return: list of incidents
        :rtype: list[Incident]
        """
        url = self.ep('all-scheduled-maintenances')
        data = self.session.rest_get(url=url)
        return TypeAdapter(list[Incident]).validate_python(data['scheduled_maintenances'])
