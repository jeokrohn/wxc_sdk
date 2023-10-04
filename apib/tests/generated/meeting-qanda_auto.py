from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AnswerObject', 'ListAnswersOfAQuestionResponse', 'ListMeetingQAndAResponse', 'QAObject', 'QAObjectAnswers', 'QAObjectAnswersLinks']


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
    #: A unique identifier for the [meeting instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) to which the Q&A belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: The total number of attendees in the meeting.
    #: example: 10.0
    total_attendees: Optional[int] = None
    #: The total number of respondents in the meeting.
    #: example: 10.0
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


class ListMeetingQAndAResponse(ApiModel):
    #: An array of Q&A objects.
    items: Optional[list[QAObject]] = None


class ListAnswersOfAQuestionResponse(ApiModel):
    #: An array of answers to a specific question.
    items: Optional[list[AnswerObject]] = None
