"""
Meetings Q and A API
"""
from collections.abc import Generator
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import LinkRelation

__all__ = ['AnswerObject', 'Answers', 'MeetingQandAApi', 'QAObject']


class AnswerObject(ApiModel):
    #: The name of the person who answered the question.
    display_name: Optional[str]
    #: The email of the person who answered the question.
    email: Optional[str]
    #: The ID of the person who answered the question. Only present for authenticated users.
    person_id: Optional[str]
    #: The content of the answer.
    answer: Optional[list[str]]
    #: Whether or not the question was answered.
    answered: Optional[bool]


class Answers(ApiModel):
    #: The pagination links of the question's answers.
    links: Optional[LinkRelation]
    #: An array of answer objects for this question.
    items: Optional[list[AnswerObject]]


class QAObject(ApiModel):
    #: A unique identifier for the question.
    id: Optional[str]
    #: A unique identifier for the meeting instance to which the Q&A belongs.
    meeting_id: Optional[str]
    #: The total number of attendees in the meeting.
    total_attendees: Optional[int]
    #: The total number of respondents in the meeting.
    total_respondents: Optional[int]
    #: The name of the user who asked the question.
    display_name: Optional[str]
    #: The email of the user who asked the question.
    email: Optional[str]
    #: The question that was asked.
    question: Optional[str]
    #: Question's answers.
    answers: Optional[Answers]


class MeetingQandAApi(ApiChild, base='meetings/q_and_a'):
    """
    During a Question and Answer (Q&A) session, attendees can pose questions to hosts, co-hosts, and presenters, who
    can answer and moderate those questions. You use the Meeting Q&A API to retrieve the questions and the answers in a
    meeting.
    Currently, these APIs are available to users with one of the meeting host, admin or Compliance Officer roles.
    The features and APIs described here are available upon-request and is not enabled by default. If would like this
    feature enabled for your organization please contact the Webex Developer Support team at devsupport@webex.com.
    """

    def list(self, meeting_id: str, **params) -> Generator[QAObject, None, None]:
        """
        Lists questions and answers from a meeting, when ready.
        Notes:

        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-meeting-q-and-a
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=QAObject, params=params)

    def list_answers(self, question_id: str, meeting_id: str,
                     **params) -> Generator[AnswerObject, None, None]:
        """
        Lists the answers to a specific question asked in a meeting.

        :param question_id: The ID of a question.
        :type question_id: str
        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-answers-of-a-question
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{question_id}/answers')
        return self.session.follow_pagination(url=url, model=AnswerObject, params=params)
