from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnswerObject', 'MeetingQAndAApi', 'QAObject', 'QAObjectAnswers', 'QAObjectAnswersLinks']


class QAObjectAnswersLinks(ApiModel):
    #: Link to the previous page of answers to this question.
    #: example: https://webexapis.com/v1/meetings/q_and_a/d513da2b-547b-4c69-b717-d83c6b02b657_M_7b789da198e531ce0c4d84243abd9fee_I_231245894851233679/answers?meetingId=7b789da198e531ce0c4d84243abd9fee_I_231245894851233679&offset=0&max=10
    prev: Optional[str] = None
    #: Link to the current page of this answers to this question.
    #: example: https://webexapis.com/v1/meetings/q_and_a/d513da2b-547b-4c69-b717-d83c6b02b657_M_7b789da198e531ce0c4d84243abd9fee_I_231245894851233679/answers?meetingId=7b789da198e531ce0c4d84243abd9fee_I_231245894851233679&offset=10&max=10
    self: Optional[str] = None
    #: Link to the next page of answers to this question.
    #: example: https://webexapis.com/v1/meetings/q_and_a/d513da2b-547b-4c69-b717-d83c6b02b657_M_7b789da198e531ce0c4d84243abd9fee_I_231245894851233679/answers?meetingId=7b789da198e531ce0c4d84243abd9fee_I_231245894851233679&offset=20&max=10
    next: Optional[str] = None


class AnswerObject(ApiModel):
    #: The name of the person who answered the question.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The email of the person who answered the question.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: The ID of the person who answered the question. Only present for authenticated users.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xYTY5MmE2Mi00MTNmLTRjYWEtYjdkOS0wYzg0ZDZmMDdlNzY
    person_id: Optional[str] = None
    #: The content of the answer.
    #: example: ['Fine, thank you.']
    answer: Optional[list[str]] = None
    #: Whether or not the question was answered.
    #: example: True
    answered: Optional[bool] = None


class QAObjectAnswers(ApiModel):
    #: The pagination links of the question's answers.
    links: Optional[QAObjectAnswersLinks] = None
    #: An array of answer objects for this question.
    items: Optional[list[AnswerObject]] = None


class QAObject(ApiModel):
    #: A unique identifier for the question.
    #: example: 1aea8390-e375-4547-b7ff-58ecd9e0b03d
    id: Optional[str] = None
    #: A unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the Q&A belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: The total number of attendees in the meeting.
    #: example: 10
    total_attendees: Optional[int] = None
    #: The total number of respondents in the meeting.
    #: example: 10
    total_respondents: Optional[int] = None
    #: The name of the user who asked the question.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The email of the user who asked the question.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: The question that was asked.
    #: example: Are you ok?
    question: Optional[str] = None
    #: Question's answers.
    answers: Optional[QAObjectAnswers] = None


class MeetingQAndAApi(ApiChild, base='meetings/q_and_a'):
    """
    Meeting Q and A
    
    During a `Question and Answer
    <https://help.webex.com/en-us/article/nakt8px/Question-and-answer-(Q&A>`_-sessions-in-Webex-Meetings-and-Webex-Webinars) (Q&A) session, attendees can pose
    questions to hosts, co-hosts, and presenters, who can answer and moderate those questions. You use the Meeting Q&A
    API to retrieve the questions and the answers in a meeting.
    
    Currently, these APIs are available to users with one of the meeting host,
    admin or `Compliance Officer
    <https://developer.webex.com/docs/compliance#compliance>`_ roles.
    
    
    
    The features and APIs described here are available upon-request and is not
    enabled by default. If would like this feature enabled for your organization
    please contact the Webex Developer Support team at devsupport@webex.com.
    
    """

    def list_meeting_q_and_a(self, meeting_id: str, **params) -> Generator[QAObject, None, None]:
        """
        List Meeting Q and A

        Lists questions and answers from a meeting, when ready.

        Notes:

        * Only `meeting instances
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ in state `ended` or `inProgress` are supported for `meetingId`.

        * Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * This API is paginated by the sum of answers in a meeting, These pagination links are returned in the response
        header.

        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the Q&A belongs to.
        :type meeting_id: str
        :return: Generator yielding :class:`QAObject` instances
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=QAObject, item_key='items', params=params)

    def list_answers_of_a_question(self, meeting_id: str, question_id: str,
                                   **params) -> Generator[AnswerObject, None, None]:
        """
        List Answers of a Question

        Lists the answers to a specific question asked in a meeting.

        * Only `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ in state `ended` or `inProgress` are supported for `meetingId`.

        * Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the Q&A belongs to.
        :type meeting_id: str
        :param question_id: The ID of a question.
        :type question_id: str
        :return: Generator yielding :class:`AnswerObject` instances
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{question_id}/answers')
        return self.session.follow_pagination(url=url, model=AnswerObject, item_key='items', params=params)
