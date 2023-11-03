from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AnswerSummaryItem', 'Link', 'Option', 'Poll', 'PollCollectionResponse', 'PollResult',
            'PollResultCollectionResponse', 'Question', 'QuestionResult', 'QuestionType', 'Respondent',
            'RespondentCollectionResponse', 'RespondentsReferenceLinks']


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
    order: Optional[datetime] = None
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
    order: Optional[datetime] = None
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
    #: A unique identifier for the [meeting
    #: instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) to which the poll belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: The date and time the poll started in https://en.wikipedia.org/wiki/ISO_8601 compliant format.
    #: example: 2021-07-06T09:22:34Z
    start_time: Optional[datetime] = None
    #: The date and time the poll ended in https://en.wikipedia.org/wiki/ISO_8601 compliant format.
    #: example: 2021-07-06T09:25:51Z
    end_time: Optional[datetime] = None
    #: The length of time in the alarm box, in seconds.
    #: example: 300.0
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


class PollCollectionResponse(ApiModel):
    items: Optional[list[Poll]] = None


class AnswerSummaryItem(ApiModel):
    #: The order of the answer in the question.
    #: example: 1
    order: Optional[datetime] = None
    #: The content of the answer.
    #: example: China
    value: Optional[str] = None
    #: The total number of people who selected this answer.
    #: example: 10.0
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
    order: Optional[datetime] = None
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
    #: A unique identifier for the [meeting
    #: instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) to which the poll belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: The total number of attendees in the meeting.
    #: example: 10.0
    total_attendees: Optional[int] = None
    #: The total number of respondents in the poll.
    #: example: 10.0
    total_respondents: Optional[int] = None
    #: The date and time the poll started in https://en.wikipedia.org/wiki/ISO_8601 compliant format.
    #: example: 2021-07-06T09:25:34Z
    start_time: Optional[datetime] = None
    #: The date and time the poll ended in https://en.wikipedia.org/wiki/ISO_8601 compliant format.
    #: example: 2021-07-06T09:28:34Z
    end_time: Optional[datetime] = None
    #: The duration of the poll, in seconds.
    #: example: 300.0
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


class PollResultCollectionResponse(ApiModel):
    items: Optional[list[PollResult]] = None


class RespondentCollectionResponse(ApiModel):
    items: Optional[list[Respondent]] = None
