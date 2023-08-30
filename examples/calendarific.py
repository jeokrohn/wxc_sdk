"""
partial Python implementation for the Calendarific API: https://calendarific.com/ using pydantic for deserialization of
results into Python objects.
To use the API you need an API key. There are various pricing models: https://calendarific.com/pricing
"""
import os
from datetime import date
from typing import Literal, List, Union, Any

import requests
from pydantic import BaseModel, Field, TypeAdapter, field_validator

HolidayType = Literal['national', 'local', 'religious', 'observance']


class Country(BaseModel):
    country_id: str = Field(alias='id')
    name: str


AllOrAny = Union[Literal['All'], Any]


class ApiError(Exception):
    pass


class Holiday(BaseModel):
    name: str
    description: str
    country: Country
    date: date
    holiday_type: List[str] = Field(alias='type')
    locations: AllOrAny  # quick and dirty. Don't need more detail right now
    states: AllOrAny  # quick and dirty. Don't need more detail right now

    @field_validator('date', mode='before')
    def validate_date(cls, v):
        data = v['datetime']
        r = date(day=data['day'], month=data['month'], year=data['year'])
        return r


class CalendarifiyApi:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('CALENDARIFIC_KEY')
        if not self.api_key:
            raise ValueError('API key needs to be passed or present in CALENDARIFIC_KEY environment variable')

    def holidays(self, *, country: str, year: int, day: int = None, month: int = None, location: str = None,
                 holiday_type: HolidayType = None) -> List[Holiday]:
        """
        This provides a list of holidays based on the parameters passed to it.
        https://calendarific.com/api-documentation

        :param country: The country parameter must be in the iso-3166 format as specified in the document here. To
            view a list of countries and regions we support, visit our list of supported countries.
        :type country: str
        :param year: The year you want to return the holidays. We currently support both historical and future years
            until 2049. The year must be specified as a number eg, 2019
        :type year: int
        :param day: Limits the number of holidays to a particular day. Must be passed as the numeric value of the
            day [1..31].
        :type day: int
        :param month: Limits the number of holidays to a particular month. Must be passed as the numeric value of the
            month [1..12].
        :type month: int
        :param location: We support multiple counties, states and regions for all the countries we support. This
            optional parameter allows you to limit the holidays to a particular state or region. The value of field
            is iso-3166 format of the state. View a list of supported countries and states. An example is, for New York
            state in the United States, it would be us-nyc
        :type location: str
        :param holiday_type: We support multiple types of holidays and observances. This parameter allows users to
            return only a particular type of holiday or event. By default, the API returns all holidays. Below is the
            list of holiday types supported by the API and this is how to reference them.
            * national - Returns public, federal and bank holidays
            * local - Returns local, regional and state holidays
            * religious - Return religious holidays: buddhism, christian, hinduism, muslim, etc
            * observance - Observance, Seasons, Times
        :type holiday_type: HolidayType
        :return: list of holidays
        :rtype: List[Holiday]
        """
        params = {k: v for i, (k, v) in enumerate(locals().items())
                  if i and v is not None and k != 'holiday_type'}
        params['api_key'] = self.api_key
        if holiday_type:
            params['type'] = holiday_type

        r = requests.get('https://calendarific.com/api/v2/holidays', params=params)
        r.raise_for_status()
        data = r.json()
        code = data['meta']['code']
        if code != 200:
            raise ApiError(data['meta']['code'], data['meta']['error_type'], data['meta']['error_detail'])
        result = TypeAdapter(list[Holiday]).validate_python(data['response']['holidays'])
        return result
