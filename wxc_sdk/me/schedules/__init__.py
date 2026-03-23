from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['MeSchedulesApi']

from wxc_sdk.base import enum_str
from wxc_sdk.common.schedules import Event, Schedule, ScheduleType


class MeSchedulesApi(ApiChild, base='telephony/config/people/me'):
    def get_location_schedule(self, schedule_type: ScheduleType, schedule_id: str) -> Schedule:
        """
        Get User's Location Level Schedule

        Get Location Schedule for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        :type schedule_type: ScheduleType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :rtype: :class:`Schedule`
        """
        url = self.ep(f'locations/schedules/{schedule_type}/{schedule_id}')
        data = super().get(url)
        r = Schedule.model_validate(data)
        return r

    def list(self) -> list[Schedule]:
        """
        Get User (and Location) Schedules

        Get Schedules for Call Settings for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[UserSchedule]
        """
        url = self.ep('schedules')
        data = super().get(url)
        r = TypeAdapter(list[Schedule]).validate_python(data['schedules'])
        return r

    def create(self, schedule: Schedule) -> str:
        """
        Add a User level Schedule for Call Settings

        Create a new Schedule for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule: Schedule details
        :type schedule: Schedule
        :rtype: str
        """
        body = schedule.create_update()
        url = self.ep('schedules')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete(self, schedule_type: ScheduleType, schedule_id: str):
        """
        Delete a User Schedule

        Delete a specific schedule for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_type: Type of the schedule.
        :type schedule_type: ScheduleType
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :rtype: None
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}')
        super().delete(url)

    def get_user_schedule(self, schedule_type: ScheduleType, schedule_id: str) -> Schedule:
        """
        Get User Schedule

        Get a Schedule details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        :type schedule_type: ScheduleType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :rtype: :class:`UserScheduleGetResponse`
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}')
        data = super().get(url)
        r = Schedule.model_validate(data)
        return r

    def update(self, schedule: Schedule, schedule_type: ScheduleType = None, schedule_id: str = None):
        """
        Modify User Schedule

        Modify a Schedule details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule: Schedule details
        :type schedule: Schedule
        :param schedule_type: Type of the schedule. Default: schedule_type from schedule
        :type schedule_type: ScheduleType
        :param schedule_id: Update the schedule with the matching ID. Default: schedule_id from schedule
        :type schedule_id: str
        :rtype: None
        """
        schedule_type = schedule_type or schedule.schedule_type
        schedule_id = schedule_id or schedule.schedule_id
        body = schedule.create_update(update=True)
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}')
        super().put(url, json=body)

    def event_create(self, schedule_type: ScheduleType, schedule_id: str, event: Event) -> str:
        """
        Add an event for a User Schedule

        Create a new Event for the authenticated user's specified schedule.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_type: Type of the schedule.
        :type schedule_type: ScheduleType
        :param schedule_id: add an event for the specified schedule ID.
        :type schedule_id: str
        :param event: Event details
        :type event: Event
        :rtype: str
        """
        body = event.create_update()
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def event_delete(self, schedule_type: ScheduleType, schedule_id: str, event_id: str):
        """
        Delete User a Schedule Event

        Delete a specific schedule event for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_type: Type of the schedule.
        :type schedule_type: ScheduleType
        :param schedule_id: Delete an event for the specified schedule ID.
        :type schedule_id: str
        :param event_id: Delete the event with the matching ID.
        :type event_id: str
        :rtype: None
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events/{event_id}')
        super().delete(url)

    def event_get(self, schedule_type: ScheduleType, schedule_id: str, event_id: str) -> Event:
        """
        Get User Schedule Event

        Get a Schedule Event details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.

            * `businessHours` - Business hours schedule type.
            * `holidays` - Holidays schedule type.
        :type schedule_type: ScheduleType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Retrieve the event with the matching ID.
        :type event_id: str
        :rtype: :class:`Event`
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events/{event_id}')
        data = super().get(url)
        r = Event.model_validate(data)
        return r

    def event_update(self, schedule_type: ScheduleType, schedule_id: str, event: Event, event_id: str = None):
        """
        Modify User Schedule Event

        Modify a Schedule event details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.

            * `businessHours` - Business hours schedule type.
            * `holidays` - Holidays schedule type.
        :type schedule_type: ScheduleType
        :param schedule_id: Update an event for the specified schedule ID.
        :type schedule_id: str
        :param event: Event details
        :type event: Event
        :param event_id: Update the event with the matching ID. Default: event id from event
        :type event_id: str
        :rtype: None
        """
        event_id = event_id or event.event_id
        body = event.create_update(update=True)
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events/{event_id}')
        super().put(url, json=body)
