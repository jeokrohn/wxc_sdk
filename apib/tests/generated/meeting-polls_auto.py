from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnswerSummaryItem', 'Link', 'MeetingPollsApi', 'Option', 'Poll', 'PollResult', 'Question',
           'QuestionResult', 'QuestionType', 'Respondent', 'RespondentsReferenceLinks']


class QuestionType(str, Enum):
    #: A single-answer question.
    single = 'single'
    #: A multiple-answer question.
    multiple = 'multiple'
    #: A text answer.
    short = 'short'


class Option(ApiModel):
    #: The order of the option.
    #: example: 1
    order: Optional[str] = None
    #: The value of the option.
    #: example: China
    value: Optional[str] = None
    #: Whether or not the option is correct.
    #: example: True
    is_correct: Optional[bool] = None


class Question(ApiModel):
    #: A unique identifier for the question.
    #: example: 6f31147e-dd69-4ea9-8b75-2c5834b72ba2
    id: Optional[str] = None
    #: The order of the question.
    #: example: 1
    order: Optional[str] = None
    #: The question.
    #: example: Where is Webex exclusively sold through local partners?
    title: Optional[str] = None
    #: The type of the question.
    #: example: single
    type: Optional[QuestionType] = None
    #: Question's options.
    options: Optional[list[Option]] = None


class Poll(ApiModel):
    #: A unique identifier for the poll.
    #: example: 1aea8390-e375-4547-b7ff-58ecd9e0b03d
    id: Optional[str] = None
    #: A unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the poll belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: The date and time the poll started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:22:34Z
    start_time: Optional[datetime] = None
    #: The date and time the poll ended in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:25:51Z
    end_time: Optional[datetime] = None
    #: The length of time in the alarm box, in seconds.
    #: example: 300
    timer_duration: Optional[int] = None
    #: The name of the poll coordinator.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The email of the poll coordinator.
    #: example: john.andersen@example.co
    email: Optional[str] = None
    #: The ID of the polling coordinator.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xYTY5MmE2Mi00MTNmLTRjYWEtYjdkOS0wYzg0ZDZmMDdlNzY
    person_id: Optional[str] = None
    #: Poll's questions.
    questions: Optional[list[Question]] = None


class AnswerSummaryItem(ApiModel):
    #: The order of the answer in the question.
    #: example: 1
    order: Optional[str] = None
    #: The content of the answer.
    #: example: China
    value: Optional[str] = None
    #: The total number of people who selected this answer.
    #: example: 10
    total_respondents: Optional[int] = None
    #: Whether the answer is correct.
    #: example: True
    is_correct: Optional[bool] = None


class Link(ApiModel):
    #: Link to the previous question's respondents.
    #: example: https://webexapis.com/v1/meetings/polls/1d4959fe-682e-4107-a346-0e1feac7b899_M_7b789da198e531ce0c4d84243abd9fee_I_231245894851233679/questions/6f31147e-dd69-4ea9-8b75-2c5834b72ba2/respondents?meetingId=7b789da198e531ce0c4d84243abd9fee_I_231245894851233679&offset=0&max=5
    prev: Optional[str] = None
    #: Link to the current question's respondents.
    #: example: https://webexapis.com/v1/meetings/polls/1d4959fe-682e-4107-a346-0e1feac7b899_M_7b789da198e531ce0c4d84243abd9fee_I_231245894851233679/questions/6f31147e-dd69-4ea9-8b75-2c5834b72ba2/respondents?meetingId=7b789da198e531ce0c4d84243abd9fee_I_231245894851233679&offset=5&max=5
    self: Optional[str] = None
    #: Link to the next page question's respondents.
    #: example: https://webexapis.com/v1/meetings/polls/1d4959fe-682e-4107-a346-0e1feac7b899_M_7b789da198e531ce0c4d84243abd9fee_I_231245894851233679/questions/6f31147e-dd69-4ea9-8b75-2c5834b72ba2/respondents?meetingId=7b789da198e531ce0c4d84243abd9fee_I_231245894851233679&offset=10&max=5
    next: Optional[str] = None


class Respondent(ApiModel):
    #: The name of the person who answers the question.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The email of the person who answers the question.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: An array of answers. Single answer or text questions contain only a single answer.
    #: example: ['Green']
    answers: Optional[list[str]] = None


class RespondentsReferenceLinks(ApiModel):
    #: The pagination links of this question's respondent.
    links: Optional[Link] = None
    #: An array of answers.
    items: Optional[list[Respondent]] = None


class QuestionResult(ApiModel):
    #: A unique identifier of the question.
    #: example: 6f31147e-dd69-4ea9-8b75-2c5834b72ba2
    id: Optional[str] = None
    #: The order of the question in the poll.
    #: example: 1
    order: Optional[str] = None
    #: The question.
    #: example: What colors do you like?
    title: Optional[str] = None
    #: The type of the question.
    #: example: single
    type: Optional[QuestionType] = None
    #: Summary of all answers.
    answer_summary: Optional[list[AnswerSummaryItem]] = None
    #: Question's respondents.
    respondents: Optional[RespondentsReferenceLinks] = None


class PollResult(ApiModel):
    #: A unique identifier for the poll.
    #: example: 1aea8390-e375-4547-b7ff-58ecd9e0b03d
    id: Optional[str] = None
    #: A unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the poll belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: The total number of attendees in the meeting.
    #: example: 10
    total_attendees: Optional[int] = None
    #: The total number of respondents in the poll.
    #: example: 10
    total_respondents: Optional[int] = None
    #: The date and time the poll started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:25:34Z
    start_time: Optional[datetime] = None
    #: The date and time the poll ended in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:28:34Z
    end_time: Optional[datetime] = None
    #: The duration of the poll, in seconds.
    #: example: 300
    timer_duration: Optional[int] = None
    #: The name of the poll coordinator.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The email of the poll coordinator.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: The ID of the the poll coordinator.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xYTY5MmE2Mi00MTNmLTRjYWEtYjdkOS0wYzg0ZDZmMDdlNzY
    person_id: Optional[str] = None
    #: An array of questions in this poll.
    questions: Optional[list[QuestionResult]] = None


class MeetingPollsApi(ApiChild, base='meetings'):
    """
    Meeting Polls
    
    As a presenter, you can use a poll to create and share questionnaires. Polls can be useful for gathering feedback,
    taking votes, or testing knowledge.
    
    You can use the Meeting Poll API to list meeting polls, the poll's questions, and answers.
    
    Currently, these APIs are available to users with one of the meeting host,
    admin or `Compliance Officer
    <https://developer.webex.com/docs/compliance#compliance>`_ roles. The polls,
    polls results, and the list of poll respondents are available within 15
    minutes following the meeting.
    
    
    
    The Webex meetings poll functionality and API endpoint described here is
    "upon-request" and not enabled by default. If you need it enabled for your
    org, or if you need help, please contact the Webex Developer Support team at
    devsupport@webex.com.
    
    """

    def list_meeting_polls(self, meeting_id: str) -> list[Poll]:
        """
        List Meeting Polls

        Lists all the polls and the poll questions in a meeting when ready.

        * Only `meeting instances
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ in state `ended` or `inProgress` are supported for `meetingId`.

        * No pagination for this API because we don't expect a large number of questions for each meeting.

        <div><Callout type="info">Polls are available within 15 minutes following the meeting.</Callout></div>

        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the polls belong.
        :type meeting_id: str
        :rtype: list[Poll]
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep('polls')
        data = super().get(url, params=params)
        r = TypeAdapter(list[Poll]).validate_python(data['items'])
        return r

    def get_meeting_poll_results(self, meeting_id: str, **params) -> Generator[PollResult, None, None]:
        """
        Get Meeting PollResults

        List the meeting polls, the poll's questions, and answers from the meeting when ready.

        * Only `meeting instances
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ in state `ended` or `inProgress` are supported for `meetingId`.

        * Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * This API is paginated by the sum of respondents from all questions in a meeting, these pagination links are
        returned in the response header.

        <div><Callout type="info">Polls results are available within 15 minutes following the meeting.</Callout></div>

        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the polls belong.
        :type meeting_id: str
        :return: Generator yielding :class:`PollResult` instances
        """
        params['meetingId'] = meeting_id
        url = self.ep('pollResults')
        return self.session.follow_pagination(url=url, model=PollResult, item_key='items', params=params)

    def list_respondents_of_a_question(self, poll_id: str, question_id: str, meeting_id: str,
                                       **params) -> Generator[Respondent, None, None]:
        """
        List Respondents of a Question

        Lists the respondents to a specific questions in a poll.

        * Only `meeting instances
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ in state `ended` or `inProgress` are supported for `meetingId`.

        * Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        <div><Callout type="info">The list of poll respondents are available within 15 minutes following the
        meeting.</Callout></div>

        :param poll_id: A unique identifier for the poll to which the respondents belong.
        :type poll_id: str
        :param question_id: A unique identifier for the question to which the respondents belong.
        :type question_id: str
        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the respondents belong.
        :type meeting_id: str
        :return: Generator yielding :class:`Respondent` instances
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'polls/{poll_id}/questions/{question_id}/respondents')
        return self.session.follow_pagination(url=url, model=Respondent, item_key='items', params=params)
