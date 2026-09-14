from __future__ import annotations

import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AIReceptionistApi', 'AiAgent', 'AiEngine', 'AiEngineName', 'AiReceptionist', 'AiReceptionistIntent',
           'AiReceptionistIntentDetails', 'AiReceptionistLocation', 'AiReceptionistResponse',
           'AiReceptionistTemplate', 'AiReceptionistTemplateListResponse', 'AlternateNumber', 'AudioFile',
           'AudioFileLevel', 'AudioFileMediaFileType', 'AvailableNumber', 'AvailableNumberState',
           'AvailableNumberTelephonyType', 'DefaultAction', 'DirectLineCallerIdName',
           'DirectLineCallerIdNameDirectLineCallerIdNameSelection', 'IntentTransferTo', 'IntentTransferToContactType',
           'IntentTransferToRequest', 'KnowledgeBaseDocument', 'KnowledgeBaseDocumentDetails',
           'KnowledgeBaseDocumentDetailsKnowledgeType', 'KnowledgeBaseDocumentDetailsStatus',
           'KnowledgeBaseMappedBot', 'KnowledgeBaseSummary', 'MessageMetadata', 'MessageText', 'Meta',
           'SessionObject', 'SessionObjectState', 'SessionsResponse', 'ToolInvocation', 'TranscriptObject',
           'TranscriptObjectUserType', 'TranscriptsResponse', 'TransparencySettings', 'TransparencySettingsResponse',
           'UpdateAiAgent', 'UpdateAiGuidelines', 'UpdateAiVoice', 'UpdateAlternateNumber',
           'UpdateAlternateNumberRingPattern', 'UpdateDefaultAction', 'UpdateDefaultActionActionType',
           'UpdateDefaultActionAudioMessageSelection', 'Voice', 'VoiceGender']


class AiReceptionistLocation(ApiModel):
    #: Unique identifier for the location of the AI receptionist.
    id: Optional[str] = None
    #: Location name of AI Receptionist.
    name: Optional[str] = None


class AiReceptionist(ApiModel):
    #: Unique identifier for the AI receptionist.
    id: Optional[str] = None
    #: Name of the AI receptionist. Must be unique within a location.
    name: Optional[str] = None
    #: Phone number of the AI receptionist in E.164 format.
    phone_number: Optional[str] = None
    #: Extension of the AI Receptionist.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of the AI Receptionist. If the location has no routing prefix, this will only be the
    #: extension. If the AI Receptionist has no extension, this field will not be present.
    esn: Optional[str] = None
    #: Location of the AI Receptionist.
    location: Optional[AiReceptionistLocation] = None


class AiReceptionistTemplateListResponse(ApiModel):
    #: Default transparency disclosure message for AI Receptionist. This message explicitly informs callers they are
    #: interacting with an AI system, ensuring compliance with EU AI Act transparency obligations for Limited Risk AI
    #: systems.
    default_transparency_message: Optional[str] = None
    #: List of AI Receptionist templates.
    templates: Optional[list[AiReceptionistLocation]] = None


class AiReceptionistTemplate(ApiModel):
    #: Unique identifier for the AI receptionist template.
    id: Optional[str] = None
    #: Name of the AI Receptionist template.
    name: Optional[str] = None
    #: Goal of the AI Receptionist.
    goal: Optional[str] = None
    #: Welcome message to be played before the call handling.
    welcome_message: Optional[str] = None
    #: Guidelines for the AI receptionist to follow. This includes information like identity, role definition, context,
    #: behavior, etc.
    guideline: Optional[str] = None
    #: Default transparency disclosure message for AI Receptionist. This message explicitly informs callers they are
    #: interacting with an AI system, ensuring compliance with EU AI Act transparency obligations for Limited Risk AI
    #: systems.
    default_transparency_message: Optional[str] = None


class AvailableNumberState(str, Enum):
    active = 'ACTIVE'
    inactive = 'INACTIVE'


class AvailableNumberTelephonyType(str, Enum):
    pstn_number = 'PSTN_NUMBER'


class AvailableNumber(ApiModel):
    #: Phone number available for assignment in E.164 format.
    phone_number: Optional[str] = None
    #: State of the phone number.
    #: - ACTIVE - Number is available to be assigned.
    #: - INACTIVE - Number is not available for assignment.
    state: Optional[AvailableNumberState] = None
    #: Flag to indicate if the number is the main number for the location.
    is_main_number: Optional[bool] = None
    #: Defines the number type.
    #: - PSTN_NUMBER - Public switched telephone network number.
    telephony_type: Optional[AvailableNumberTelephonyType] = None
    #: Flag to indicate if the number is toll free.
    toll_free_number: Optional[bool] = None
    #: Flag to indicate if the number is Service Number.
    is_service_number: Optional[bool] = None


class IntentTransferToContactType(str, Enum):
    people = 'PEOPLE'
    resource_group = 'RESOURCE_GROUP'
    contact = 'CONTACT'
    phone_number = 'PHONE_NUMBER'


class IntentTransferTo(ApiModel):
    #: Type of transfer destination.
    #: - PEOPLE - A person in the organization.
    #: - RESOURCE_GROUP - A group resource such as a call queue or hunt group.
    #: - CONTACT - An organization contact.
    #: - PHONE_NUMBER - A raw phone number or extension.
    contact_type: Optional[IntentTransferToContactType] = None
    #: Unique identifier for the transfer destination, encoded using the resource type indicated by contactType
    #: (PEOPLE, RESOURCE_GROUP, or CONTACT). Not required when contactType is PHONE_NUMBER.
    contact_id: Optional[str] = None
    #: Name of the calling service or contact.
    name: Optional[str] = None
    #: Phone number of calling service or contact.
    phone_number: Optional[str] = None


class AiReceptionistIntent(ApiModel):
    #: Unique identifier of the intent.
    id: Optional[str] = None
    #: Name of the intent.
    name: Optional[str] = None
    #: Transfer destination for the intent.
    transfer_to: Optional[IntentTransferTo] = None


class IntentTransferToRequest(ApiModel):
    #: Contact type.
    #: - PEOPLE - A person in the organization.
    #: - RESOURCE_GROUP - A group resource such as a call queue or hunt group.
    #: - CONTACT - An organization contact.
    #: - PHONE_NUMBER - A raw phone number or extension.
    contact_type: Optional[IntentTransferToContactType] = None
    #: Unique identifier for the transfer destination, encoded using the resource type indicated by contactType
    #: (PEOPLE, RESOURCE_GROUP, or CONTACT). Not required when contactType is PHONE_NUMBER.
    contact_id: Optional[str] = None
    #: Phone number for intent transfer.
    phone_number: Optional[str] = None


class AiReceptionistIntentDetails(ApiModel):
    #: Unique identifier for a specific AI Receptionist intent within a given location and AI Receptionist instance.
    id: Optional[str] = None
    #: Name of the intent.
    name: Optional[str] = None
    #: Description of the intent (Action).
    description: Optional[str] = None
    transfer_to: Optional[IntentTransferTo] = None


class AiEngineName(str, Enum):
    pro = 'PRO'
    pro_us = 'PRO_US'


class VoiceGender(str, Enum):
    male = 'MALE'
    female = 'FEMALE'


class Voice(ApiModel):
    #: Voice language.
    language: Optional[str] = None
    #: Voice locale code.
    language_code: Optional[str] = None
    #: Voice display name.
    display_name: Optional[str] = None
    #: Field to indicate default voice.
    is_default: Optional[bool] = None
    #: Voice gender.
    #: - MALE — Male voice.
    #: - FEMALE — Female voice.
    gender: Optional[VoiceGender] = None


class AiEngine(ApiModel):
    #: AI engine name.
    #: - PRO — Available in all supported countries.
    #: - PRO_US — Available in the United States only.
    name: Optional[AiEngineName] = None
    #: List of available voices for this AI engine.
    voices: Optional[list[Voice]] = None


class DirectLineCallerIdNameDirectLineCallerIdNameSelection(str, Enum):
    display_name = 'DISPLAY_NAME'
    custom_name = 'CUSTOM_NAME'


class DirectLineCallerIdName(ApiModel):
    #: Field to indicate the option chosen to represent the Caller ID:
    #: 
    #: - `DISPLAY_NAME` - Use the AI Receptionist display name as the caller ID.
    #: - `CUSTOM_NAME` - Use a custom name as the caller ID.
    direct_line_caller_id_name_selection: Optional[DirectLineCallerIdNameDirectLineCallerIdNameSelection] = None
    #: Carries the customized name when "CUSTOM_NAME" is the chosen option. It can be empty if it's not configured.
    custom_name: Optional[str] = None


class UpdateDefaultActionActionType(str, Enum):
    play_message_and_disconnect = 'PLAY_MESSAGE_AND_DISCONNECT'
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'


class UpdateDefaultActionAudioMessageSelection(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'


class UpdateDefaultAction(ApiModel):
    #: Default action to be played when call is first received:
    #: 
    #: - `PLAY_MESSAGE_AND_DISCONNECT` - Play an audio message and disconnect the call.
    #: - `TRANSFER_TO_OPERATOR` - Transfer the call to an operator.
    action_type: Optional[UpdateDefaultActionActionType] = None
    #: Announcement type to be played. Mandatory if actionType is `PLAY_MESSAGE_AND_DISCONNECT`:
    #: 
    #: - `DEFAULT` - Use the system default audio message.
    #: - `CUSTOM` - Use a custom uploaded audio file.
    audio_message_selection: Optional[UpdateDefaultActionAudioMessageSelection] = None
    #: Audio message file ID which is already uploaded. Mandatory if audioMessageSelection is CUSTOM
    audio_file_id: Optional[str] = None
    #: Phone number or extension to transfer call to. Mandatory if actionType is `TRANSFER_TO_OPERATOR`.
    transfer_to_number: Optional[str] = None
    #: Transfer target configuration. Alternative to transferToNumber
    transfer_to: Optional[IntentTransferToRequest] = None


class UpdateAiVoice(ApiModel):
    #: AI engine name.
    #: 
    #: - `PRO` — Available in all supported countries.
    #: - `PRO_US` — Available in the United States only.
    ai_engine: Optional[AiEngineName] = None
    #: Display name of the AI Receptionist voice.
    display_name: Optional[str] = None
    #: Voice language name
    language: Optional[str] = None
    #: Voice language locale in BCP 47 format
    language_code: Optional[str] = None


class UpdateAiGuidelines(ApiModel):
    #: Goal of the AI Receptionist. The combined length of `goal` and `guideline` must not exceed 5096 characters.
    goal: Optional[str] = None
    #: Welcome message to be played before the call handling.
    welcome_message: Optional[str] = None
    #: Guidelines to AI Receptionist to follow. This includes information like Identity, role definition, context,
    #: behavior etc.. The combined length of `goal` and `guideline` must not exceed 5096 characters.
    guideline: Optional[str] = None


class TransparencySettings(ApiModel):
    #: Flag to enable or disable transparency disclosure for AI Receptionist.
    enabled: Optional[bool] = None
    #: Custom transparency message to inform callers they are interacting with an AI system.
    message: Optional[str] = None
    #: Reason for disabling transparency disclosure.
    disable_reason: Optional[str] = None


class UpdateAiAgent(ApiModel):
    #: Voice configuration for the AI Agent
    voice: Optional[UpdateAiVoice] = None
    #: Unique identifier for the Knowledge Base used by the AI Agent to answer caller queries.
    knowledge_base_id: Optional[str] = None
    #: AI Agent guidelines
    guidelines: Optional[UpdateAiGuidelines] = None
    #: Transparency settings for AI Receptionist. Configures disclosure messages to inform callers they are interacting
    #: with an AI system, ensuring compliance with EU AI Act transparency obligations.
    transparency_settings: Optional[TransparencySettings] = None


class UpdateAlternateNumberRingPattern(str, Enum):
    normal = 'NORMAL'
    long_long = 'LONG_LONG'
    short_short_long = 'SHORT_SHORT_LONG'
    short_long_short = 'SHORT_LONG_SHORT'


class UpdateAlternateNumber(ApiModel):
    #: Alternate phone number.
    phone_number: Optional[str] = None
    #: Ring pattern for the alternate number:
    #: 
    #: - `NORMAL` - Standard ring pattern.
    #: - `LONG_LONG` - Two long rings.
    #: - `SHORT_SHORT_LONG` - Two short rings followed by one long ring.
    #: - `SHORT_LONG_SHORT` - Short, long, short ring pattern.
    ring_pattern: Optional[UpdateAlternateNumberRingPattern] = None


class AlternateNumber(ApiModel):
    #: Alternate phone number.
    phone_number: Optional[str] = None
    #: Flag to indicate if the number is toll free number
    toll_free_number: Optional[bool] = None
    #: Ring pattern for the alternate number:
    #: 
    #: - `NORMAL` - Standard ring pattern.
    #: - `LONG_LONG` - Two long rings.
    #: - `SHORT_SHORT_LONG` - Two short rings followed by one long ring.
    #: - `SHORT_LONG_SHORT` - Short, long, short ring pattern.
    ring_pattern: Optional[UpdateAlternateNumberRingPattern] = None


class AudioFileMediaFileType(str, Enum):
    wav = 'WAV'


class AudioFileLevel(str, Enum):
    organization = 'ORGANIZATION'
    location = 'LOCATION'
    entity = 'ENTITY'


class AudioFile(ApiModel):
    #: Audio file ID
    id: Optional[str] = None
    #: Audio file name
    file_name: Optional[str] = None
    #: Media file type.
    #: - `WAV` - WAV File Extension.
    media_file_type: Optional[AudioFileMediaFileType] = None
    #: Level at which the audio file is stored and shared.
    #: 
    #: - `ORGANIZATION` — File is shared across the entire organization.
    #: - `LOCATION` — File is scoped to a specific location.
    #: - `ENTITY` — File is scoped to a specific entity (e.g., AI Receptionist).
    level: Optional[AudioFileLevel] = None
    #: Flag indicating if this is a text-to-speech file
    is_text_to_speech: Optional[bool] = None


class DefaultAction(ApiModel):
    #: Default action to be performed when a call is received:
    #: 
    #: - `PLAY_MESSAGE_AND_DISCONNECT` - Play an audio message and disconnect the call.
    #: - `TRANSFER_TO_OPERATOR` - Transfer the call to an operator.
    action_type: Optional[UpdateDefaultActionActionType] = None
    #: Announcement type to be played. Mandatory if actionType is `PLAY_MESSAGE_AND_DISCONNECT`:
    #: 
    #: - `DEFAULT` - Use the system default audio message.
    #: - `CUSTOM` - Use a custom uploaded audio file.
    audio_message_selection: Optional[UpdateDefaultActionAudioMessageSelection] = None
    #: Audio file details. Mandatory if audioMessageSelection is CUSTOM.
    audio_file: Optional[AudioFile] = None
    #: Transfer to number. Mandatory if actionType is `TRANSFER_TO_OPERATOR`.
    transfer_to_number: Optional[str] = None
    #: Transfer target configuration. Alternative to transferToNumber
    transfer_to: Optional[IntentTransferToRequest] = None


class TransparencySettingsResponse(ApiModel):
    #: Flag to enable or disable transparency disclosure for AI Receptionist.
    enabled: Optional[bool] = None
    #: Custom transparency message to inform callers they are interacting with an AI system.
    message: Optional[str] = None


class AiAgent(ApiModel):
    #: AI Agent ID from Webex AI Agent Studio
    agent_id: Optional[str] = None
    #: Voice configuration for the AI Agent
    voice: Optional[UpdateAiVoice] = None
    #: Unique identifier for the Knowledge Base used by the AI Agent to answer caller queries.
    knowledge_base_id: Optional[str] = None
    #: AI Agent guidelines
    guidelines: Optional[UpdateAiGuidelines] = None
    #: Transparency settings for AI Receptionist. Configures disclosure messages to inform callers they are interacting
    #: with an AI system, ensuring compliance with EU AI Act transparency obligations.
    transparency_settings: Optional[TransparencySettingsResponse] = None


class AiReceptionistResponse(ApiModel):
    #: AI Receptionist ID encoded using the Resource Type.
    id: Optional[str] = None
    #: Name of the AI Receptionist. This has to be unique across location
    name: Optional[str] = None
    #: Flag to indicate AI receptionist is enabled or not. When disabled, incoming calls to this AI receptionist will
    #: not be answered.
    enabled: Optional[bool] = None
    #: Phone number of the AI Receptionist. Either phoneNumber or extension is mandatory. At least one is required.
    phone_number: Optional[str] = None
    #: Extension of the AI Receptionist. Either phoneNumber or extension is mandatory. At least one is required.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of the AI Receptionist. If the location has no routing prefix, this will only be the
    #: extension. If the AI Receptionist has no extension, this field will not be present.
    esn: Optional[str] = None
    #: List of alternate phone numbers assigned to the AI Receptionist.
    alternate_numbers: Optional[list[AlternateNumber]] = None
    #: Direct line caller ID name configuration
    direct_line_caller_id_name: Optional[DirectLineCallerIdName] = None
    #: A dial by name used for AI Receptionist name dialing. Characters of `%`, `+`, `\`, `"` and Unicode characters
    #: are not allowed.
    dial_by_name: Optional[str] = None
    #: Default action configuration for the AI Receptionist
    default_action: Optional[DefaultAction] = None
    #: AI Agent configuration
    ai_agent: Optional[AiAgent] = None
    #: Number of intents configured for this AI Receptionist
    intent_count: Optional[int] = None


class KnowledgeBaseMappedBot(ApiModel):
    #: Unique identifier for the AI Receptionist.
    id: Optional[str] = None
    #: Timestamp indicating when the Knowledge Base was associated with the AI Receptionist, in ISO 8601 format.
    connected_at: Optional[datetime] = None
    #: Unique identifier for the AI agent associated with this receptionist.
    agent_id: Optional[str] = None
    #: Name of the AI Receptionist (Bot).
    name: Optional[str] = None


class KnowledgeBaseSummary(ApiModel):
    #: Unique identifier of the Knowledge Base.
    id: Optional[str] = None
    #: The display name assigned to the Knowledge Base. Used to identify the KB across the platform.
    name: Optional[str] = None
    #: A human-readable description providing additional context about the purpose or contents of the Knowledge Base.
    description: Optional[str] = None
    #: The total count of documents that have been uploaded or indexed into the Knowledge Base.
    documents_count: Optional[int] = None
    #: The total count of files that have been uploaded to the Knowledge Base.
    files_count: Optional[int] = None
    #: The cumulative size (in bytes) of all files stored in the Knowledge Base.
    files_size: Optional[int] = None
    #: Timestamp indicating when the Knowledge Base was originally created, in ISO 8601 format.
    created_at: Optional[datetime] = None
    #: Timestamp indicating when the Knowledge Base was last modified, in ISO 8601 format.
    updated_at: Optional[datetime] = None
    #: List of AI Receptionists that are currently associated with this Knowledge Base.
    mapped_bots: Optional[list[KnowledgeBaseMappedBot]] = None


class KnowledgeBaseDocument(ApiModel):
    #: Unique identifier of the knowledge base document.
    id: Optional[str] = None
    #: Name or filename of the knowledge base document.
    name: Optional[str] = None
    #: Relevance score of the document.
    score: Optional[int] = None
    #: Extracted text content from the document.
    text: Optional[str] = None


class KnowledgeBaseDocumentDetailsKnowledgeType(str, Enum):
    article = 'article'
    file = 'file'


class KnowledgeBaseDocumentDetailsStatus(str, Enum):
    pending = 'pending'
    processing = 'processing'
    success = 'success'
    failed = 'failed'


class KnowledgeBaseDocumentDetails(ApiModel):
    #: Unique identifier for the document.
    id: Optional[str] = None
    #: Unique identifier for the Knowledge Base this document belongs to.
    knowledge_base_id: Optional[str] = None
    #: Name of the document.
    name: Optional[str] = None
    #: Content of the document.
    content: Optional[str] = None
    #: Description of the document.
    description: Optional[str] = None
    #: Original file name if the document was uploaded as a file.
    file_name: Optional[str] = None
    #: Size of the document in bytes.
    file_size: Optional[int] = None
    #: Type of knowledge content.
    #: - `article` - Text-based content created directly via API.
    #: - `file` - Content uploaded as a document file.
    knowledge_type: Optional[KnowledgeBaseDocumentDetailsKnowledgeType] = None
    #: Processing status of the document.
    #: - `pending` - Document is waiting to be processed.
    #: - `processing` - Document is currently being indexed.
    #: - `success` - Document has been successfully indexed and is available for queries.
    #: - `failed` - Document processing failed.
    status: Optional[KnowledgeBaseDocumentDetailsStatus] = None
    #: Timestamp indicating when the document was created, in ISO 8601 format.
    created_at: Optional[datetime] = None
    #: Timestamp indicating when the document was last modified, in ISO 8601 format.
    updated_at: Optional[datetime] = None


class Meta(ApiModel):
    #: Maximum number of items returned per page.
    limit: Optional[int] = None
    #: Zero-based index of the first item in the current page.
    offset: Optional[int] = None
    #: Total number of items available across all pages.
    total_count: Optional[int] = Field(alias='total_count', default=None)
    #: URL to the next page of results, or null if this is the last page.
    next: Optional[str] = None
    #: URL to the previous page of results, or null if this is the first page.
    previous: Optional[str] = None


class SessionObjectState(str, Enum):
    open = 'open'
    closed = 'closed'


class SessionObject(ApiModel):
    #: Unique session identifier. Use as `sessionId` in the transcripts API.
    id: Optional[str] = None
    #: Unique call identifier (This is same as call correlation ID in Control Hub troubleshooting).
    interaction_id: Optional[str] = Field(alias='interaction_id', default=None)
    #: State of the session.
    state: Optional[SessionObjectState] = None
    #: Creation timestamp in epoch milliseconds.
    created_at: Optional[int] = Field(alias='created_at', default=None)
    #: Last-updated timestamp in epoch milliseconds.
    updated_at: Optional[int] = Field(alias='updated_at', default=None)
    #: Indicates a test invocation. Always `false` for AI Receptionist.
    is_test: Optional[bool] = Field(alias='is_test', default=None)


class SessionsResponse(ApiModel):
    #: Pagination metadata for the response.
    meta: Optional[Meta] = None
    #: List of session objects.
    objects: Optional[list[SessionObject]] = None
    #: Unique identifier for this API transaction.
    transaction_id: Optional[str] = Field(alias='transaction_id', default=None)


class MessageText(ApiModel):
    #: Utterance text.
    text: Optional[str] = None


class ToolInvocation(ApiModel):
    #: Unique identifier of the tool.
    tool_id: Optional[str] = Field(alias='tool_id', default=None)
    #: Display name of the tool.
    tool_name: Optional[str] = Field(alias='tool_name', default=None)
    #: Type of the tool response (e.g., tool_execution_response).
    type: Optional[str] = None
    #: Capability type of the tool (e.g., custom_transfer).
    capability: Optional[str] = None
    #: Human-readable description of the tool's purpose.
    description: Optional[str] = None
    #: Execution state of the tool invocation (e.g., SUCCESS).
    state: Optional[str] = None
    #: Time in milliseconds taken to execute the tool.
    latency: Optional[int] = None
    #: Size of the tool response in bytes.
    size: Optional[int] = None
    #: Input parameters passed to the tool.
    input: Optional[dict] = None
    #: Unique identifier of the knowledge base used.
    kb_id: Optional[str] = Field(alias='kb_id', default=None)
    #: Name of the knowledge base used.
    kb_name: Optional[str] = Field(alias='kb_name', default=None)
    #: Knowledge base documents retrieved during tool execution.
    kb_docs: Optional[list[KnowledgeBaseDocument]] = Field(alias='kb_docs', default=None)
    #: Output returned by the tool.
    output: Optional[dict] = None
    #: Classification results from the tool.
    classification: Optional[list[dict]] = None
    #: Slot values collected during tool execution.
    slots: Optional[list[dict]] = None
    #: Request identifier for the tool invocation.
    request_id: Optional[str] = None
    #: Transaction identifier for the tool invocation.
    transaction_id: Optional[str] = Field(alias='transaction_id', default=None)


class MessageMetadata(ApiModel):
    #: Name of the AI engine used.
    ai_name: Optional[str] = Field(alias='ai_name', default=None)
    #: Version of the AI engine.
    ai_version: Optional[str] = Field(alias='ai_version', default=None)
    #: Unique identifier of the chat message.
    chat_message_id: Optional[str] = Field(alias='chat_message_id', default=None)
    #: Identifier of the AI engine.
    engine_identifier: Optional[str] = Field(alias='engine_identifier', default=None)
    #: Language code of the message (e.g., en-US, en-GB).
    language: Optional[str] = None
    #: Response latency in milliseconds.
    latency: Optional[int] = None
    #: Additional parameters associated with the message.
    parameters: Optional[dict] = None
    #: Size of the message in characters.
    size: Optional[int] = None
    #: List of tools invoked while processing this message.
    tools: Optional[list[ToolInvocation]] = None


class TranscriptObjectUserType(str, Enum):
    human = 'human'
    bot = 'bot'


class TranscriptObject(ApiModel):
    #: Unique identifier of the transcript message.
    id: Optional[str] = None
    #: Transaction identifier grouping related messages.
    transaction_id: Optional[str] = Field(alias='transaction_id', default=None)
    #: Indicates whether the message is from the caller (human) or the AI Receptionist (bot).
    user_type: Optional[TranscriptObjectUserType] = Field(alias='user_type', default=None)
    #: Message content. For human messages this is a string; for bot messages it is an array of text objects.
    message: Optional[Union[str, list[MessageText]]] = None
    #: Additional metadata for the message.
    metadata: Optional[MessageMetadata] = None
    #: Indicates whether an error occurred while processing this message.
    error: Optional[bool] = None
    #: Creation timestamp in epoch milliseconds.
    created_at: Optional[int] = Field(alias='created_at', default=None)
    #: Last-updated timestamp in epoch milliseconds.
    updated_at: Optional[int] = Field(alias='updated_at', default=None)


class TranscriptsResponse(ApiModel):
    #: Pagination metadata for the response.
    meta: Optional[Meta] = None
    #: List of transcript message objects.
    objects: Optional[list[TranscriptObject]] = None
    #: Unique identifier for this API transaction.
    transaction_id: Optional[str] = Field(alias='transaction_id', default=None)


class AIReceptionistApi(ApiChild, base=''):
    """
    AI Receptionist
    
    AI Receptionist for Webex Calling allows administrators to configure and manage AI-powered receptionists that
    handle incoming calls. This includes validating countries and AI receptionist names, listing available phone
    numbers, managing templates, and retrieving intents.
    
    Viewing these settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in another organization using the optional `orgId` query
    parameter.
    
    **Note:** AI Receptionist Session Transcripts APIs requires a full administrator auth token with a CI role of
    `id_full_admin`.
    """

    def list_ai_receptionist_sessions(self, ai_receptionist_id: str, interaction_id: str = None, limit: int = None,
                                      offset: int = None) -> SessionsResponse:
        """
        List AI Receptionist Sessions

        List the AI Receptionist sessions for the given `aiReceptionistId`.

        A session represents a single conversation between a caller and the AI Receptionist. You can optionally filter
        sessions by `interaction_id` (which corresponds to the call correlation ID retrievable from the Webex Control
        Hub troubleshooting page) to locate the session associated with a specific call.

        This API requires a full administrator auth token with a CI role of `id_full_admin`.

        :param ai_receptionist_id: Unique identifier of the AI Receptionist. AI Receptionist ID from the response of
            List AI Receptionists API.
        :type ai_receptionist_id: str
        :param interaction_id: Filter sessions by the call correlation ID retrieved from Webex Control Hub
            troubleshooting page.
        :type interaction_id: str
        :param limit: Maximum number of sessions to return in a single page. Must be between `1` and `100`.
        :type limit: int
        :param offset: Pagination offset. Starting index of the result set.
        :type offset: int
        :rtype: :class:`SessionsResponse`
        """
        params: dict[str, Any] = dict()
        if interaction_id is not None:
            params['interaction_id'] = interaction_id
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        url = self.ep(f'aiReceptionists/{ai_receptionist_id}/sessions')
        data = super().get(url, params=params)
        r = SessionsResponse.model_validate(data)
        return r

    def get_ai_receptionist_session_transcripts(self, ai_receptionist_id: str, session_id: str, limit: int = None,
                                                offset: int = None) -> TranscriptsResponse:
        """
        Get AI Receptionist Session Transcripts

        Retrieve the transcript (messages exchanged between the caller and the AI Receptionist) for a specific session.

        Each message represents a single utterance, identified by `user_type` (`human` or `bot`). For bot messages, the
        message is an array of text objects; for human messages, it is a plain string. Additional metadata may include
        tool invocations, knowledge-base lookups, and latency information useful for debugging.

        This API requires a full administrator auth token with a CI role of `id_full_admin`.

        :param ai_receptionist_id: Unique identifier of the AI Receptionist. AI Receptionist ID from the response of
            List AI Receptionists API.
        :type ai_receptionist_id: str
        :param session_id: Identifier of the session returned by the List AI Receptionist Sessions API.
        :type session_id: str
        :param limit: Maximum number of messages to return in a single page. Must be between `1` and `1000`.
        :type limit: int
        :param offset: Pagination offset. Starting index of the result set.
        :type offset: int
        :rtype: :class:`TranscriptsResponse`
        """
        params: dict[str, Any] = dict()
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        url = self.ep(f'aiReceptionists/{ai_receptionist_id}/sessions/{session_id}/transcripts')
        data = super().get(url, params=params)
        r = TranscriptsResponse.model_validate(data)
        return r

    def list_ai_receptionists(self, location_id: str = None, name: str = None, phone_number: str = None,
                              org_id: str = None, **params: Any) -> Generator[AiReceptionist, None, None]:
        """
        List AI Receptionists

        Get list of AI Receptionists.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls to
        people or services. These APIs let administrators manage AI receptionist resources across organizations and
        locations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location identifier. If not specified, returns AI receptionists from all locations.
        :type location_id: str
        :param name: Search AI receptionists by name (contains match).
        :type name: str
        :param phone_number: Search (Contains) based on number or extension. Search cannot be performed based on esn.
        :type phone_number: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :return: Generator yielding :class:`AiReceptionist` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('telephony/config/aiReceptionists')
        return self.session.follow_pagination(url=url, model=AiReceptionist, item_key='aiReceptionists', params=params)

    def validate_ai_receptionist_country(self, country_code: str, location_id: str = None, org_id: str = None) -> None:
        """
        Validate Country for AI Receptionist

        Validates if country passed in the request supports AI Receptionist.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param country_code: Two letter country code of the location for which AI Receptionist needs to be validated.
        :type country_code: str
        :param location_id: Location associated with the AI Receptionist.
        :type location_id: str
        :param org_id: Optional; target organization ID, otherwise defaults to token's org.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['countryCode'] = country_code
        if location_id is not None:
            body['locationId'] = location_id
        url = self.ep('telephony/config/aiReceptionists/actions/validateCountry/invoke')
        super().post(url, params=params, json=body)

    def list_ai_receptionist_templates(self, org_id: str = None) -> AiReceptionistTemplateListResponse:
        """
        List AI Receptionist Templates

        Get AI Receptionist template list.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls.
        Templates help standardize greetings, goals, and guidelines.

        Returns all templates in a single response.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`AiReceptionistTemplateListResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/aiReceptionists/templates')
        data = super().get(url, params=params)
        r = AiReceptionistTemplateListResponse.model_validate(data)
        return r

    def get_ai_receptionist_template(self, template_id: str, org_id: str = None) -> AiReceptionistTemplate:
        """
        Get AI Receptionist template details.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Use
        templates to define goals, messages, and guidelines.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param template_id: Template Id.
        :type template_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`AiReceptionistTemplate`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/aiReceptionists/templates/{template_id}')
        data = super().get(url, params=params)
        r = AiReceptionistTemplate.model_validate(data)
        return r

    def list_knowledge_bases(self, name: str = None, org_id: str = None,
                             **params: Any) -> Generator[KnowledgeBaseSummary, None, None]:
        """
        List Knowledge Bases

        Get list of Knowledge Bases for an organization.

        Knowledge Bases are repositories of information that AI Receptionists use to answer caller queries. This API
        returns all knowledge bases available in the organization.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Search knowledge bases by name (contains match).
        :type name: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :return: Generator yielding :class:`KnowledgeBaseSummary` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        url = self.ep('telephony/config/knowledgeBases')
        return self.session.follow_pagination(url=url, model=KnowledgeBaseSummary, item_key='knowledgeBases', params=params)

    def create_knowledge_base(self, name: str, description: str = None, org_id: str = None) -> str:
        """
        Create a Knowledge Base

        Create a new Knowledge Base for an organization.

        Knowledge Bases are repositories of information that AI Receptionists use to answer caller queries.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param name: The display name assigned to the Knowledge Base. Used to identify the KB across the platform.
        :type name: str
        :param description: A human-readable description providing additional context about the purpose or contents of
            the Knowledge Base.
        :type description: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        if description is not None:
            body['description'] = description
        url = self.ep('telephony/config/knowledgeBases')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_knowledge_base(self, knowledge_base_id: str, org_id: str = None) -> None:
        """
        Delete a Knowledge Base.

        Knowledge Bases are repositories of information that AI Receptionists use to answer caller queries.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}')
        super().delete(url, params=params)

    def get_knowledge_base(self, knowledge_base_id: str, org_id: str = None) -> KnowledgeBaseSummary:
        """
        Get Knowledge Base Details

        Get details of a specific Knowledge Base.

        Knowledge Bases are repositories of information that AI Receptionists use to answer caller queries.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`KnowledgeBaseSummary`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}')
        data = super().get(url, params=params)
        r = KnowledgeBaseSummary.model_validate(data)
        return r

    def update_knowledge_base(self, knowledge_base_id: str, name: str = None, description: str = None,
                              org_id: str = None) -> None:
        """
        Modify a Knowledge Base

        Modify an existing Knowledge Base.

        Knowledge Bases are repositories of information that AI Receptionists use to answer caller queries.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param name: The display name assigned to the Knowledge Base. Used to identify the KB across the platform.
        :type name: str
        :param description: A human-readable description providing additional context about the purpose or contents of
            the Knowledge Base.
        :type description: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}')
        super().put(url, params=params, json=body)

    def list_knowledge_base_documents(self, knowledge_base_id: str, org_id: str = None,
                                      **params: Any) -> Generator[KnowledgeBaseDocument, None, None]:
        """
        List Knowledge Base Documents

        Get list of documents in a Knowledge Base.

        Documents are files uploaded to a Knowledge Base that AI Receptionists use to answer caller queries.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :return: Generator yielding :class:`KnowledgeBaseDocument` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents')
        return self.session.follow_pagination(url=url, model=KnowledgeBaseDocument, item_key='documents', params=params)

    def create_knowledge_base_document(self, knowledge_base_id: str, name: str, content: str,
                                       org_id: str = None) -> str:
        """
        Create Knowledge Base Document

        Create a new document in a Knowledge Base.

        Documents are content entries in a Knowledge Base that AI Receptionists use to answer caller queries. This API
        creates a document with specified name and content.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param name: The display name assigned to the Knowledge Base document. Used to identify the document across the
            platform.
        :type name: str
        :param content: The content of the document.
        :type content: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        body['content'] = content
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def upload_knowledge_base_document(self, knowledge_base_id: str, file: str, org_id: str = None) -> str:
        """
        Upload Knowledge Base Document

        Upload a document to a Knowledge Base.

        Documents are files uploaded to a Knowledge Base that AI Receptionists use to answer caller queries. Supported
        file types include PDF, TXT, DOCX, XLSX, XLS, and CSV.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        multipart POST. This API can be utilized using other tools that support multipart POST, such as Postman.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param file: The document file to upload. Supported file types: PDF, TXT, DOCX, XLSX, XLS, CSV. Maximum file
            size: 10MB.
        :type file: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['file'] = file
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents/actions/upload/invoke')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_knowledge_base_document(self, knowledge_base_id: str, document_id: str, org_id: str = None) -> None:
        """
        Delete Knowledge Base Document

        Delete a document from a Knowledge Base.

        Documents are files uploaded to a Knowledge Base that AI Receptionists use to answer caller queries.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param document_id: Unique identifier for the document.
        :type document_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents/{document_id}')
        super().delete(url, params=params)

    def get_knowledge_base_document(self, knowledge_base_id: str, document_id: str,
                                    org_id: str = None) -> KnowledgeBaseDocumentDetails:
        """
        Get Knowledge Base Document Details

        Get details of a specific document in a Knowledge Base.

        Documents are content entries in a Knowledge Base that AI Receptionists use to answer caller queries. This API
        returns document metadata including name, content, status, and timestamps.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param document_id: Unique identifier for the document.
        :type document_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`KnowledgeBaseDocumentDetails`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents/{document_id}')
        data = super().get(url, params=params)
        r = KnowledgeBaseDocumentDetails.model_validate(data)
        return r

    def update_knowledge_base_document(self, knowledge_base_id: str, document_id: str, name: str = None,
                                       content: str = None, org_id: str = None) -> None:
        """
        Modify Knowledge Base Document

        Modify a document in a Knowledge Base.

        Documents are content entries in a Knowledge Base that AI Receptionists use to answer caller queries. This API
        allows updating the name and content of an existing document.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param document_id: Unique identifier for the document.
        :type document_id: str
        :param name: The display name assigned to the Knowledge Base document. Used to identify the document across the
            platform.
        :type name: str
        :param content: The content of the document.
        :type content: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if name is not None:
            body['name'] = name
        if content is not None:
            body['content'] = content
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents/{document_id}')
        super().put(url, params=params, json=body)

    def download_knowledge_base_document(self, knowledge_base_id: str, document_id: str, org_id: str = None) -> str:
        """
        Download Knowledge Base Document

        Download a document from a Knowledge Base.

        Documents are files uploaded to a Knowledge Base that AI Receptionists use to answer caller queries. The
        response contains the file content with appropriate Content-Type and Content-Disposition headers.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        binary file downloads. This API can be utilized using other tools that support binary responses, such as
        Postman or curl.

        :param knowledge_base_id: Unique identifier for the Knowledge Base.
        :type knowledge_base_id: str
        :param document_id: Unique identifier for the document.
        :type document_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/knowledgeBases/{knowledge_base_id}/documents/{document_id}/actions/download/invoke')
        data = super().post(url, params=params)
        r = TypeAdapter(str).validate_python(data)
        return r

    def create_ai_receptionist(self, location_id: str, name: str, enabled: bool, default_action: UpdateDefaultAction,
                               ai_agent: UpdateAiAgent, phone_number: str = None, extension: str = None,
                               direct_line_caller_id_name: DirectLineCallerIdName = None, dial_by_name: str = None,
                               org_id: str = None) -> str:
        """
        Create an AI Receptionist

        Create a new AI Receptionist for a location.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls to
        people or services.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param name: Name of the AI Receptionist. This has to be unique across location.
        :type name: str
        :param enabled: Flag to indicate AI receptionist is enabled or not. When disabled, incoming calls to this AI
            receptionist will not be answered.
        :type enabled: bool
        :param default_action: Default action configuration for the AI Receptionist
        :type default_action: UpdateDefaultAction
        :param ai_agent: AI Agent configuration
        :type ai_agent: UpdateAiAgent
        :param phone_number: Phone number of the AI Receptionist. Either phoneNumber or extension is mandatory. At
            least one is required.
        :type phone_number: str
        :param extension: Extension of the AI Receptionist. Either phoneNumber or extension is mandatory. At least one
            is required.
        :type extension: str
        :param direct_line_caller_id_name: Direct line caller ID name configuration
        :type direct_line_caller_id_name: DirectLineCallerIdName
        :param dial_by_name: A dial by name used for AI Receptionist name dialing. Characters of `%`, `+`, `\\`, `"`
            and Unicode characters are not allowed.
        :type dial_by_name: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        body['enabled'] = enabled
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        body['defaultAction'] = default_action.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['aiAgent'] = ai_agent.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def validate_ai_receptionist(self, location_id: str, name: str, org_id: str = None) -> None:
        """
        Validate AI Receptionist

        Validates AI Receptionist name at location level and max limit at org level.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param name: Name of the AI Receptionist.
        :type name: str
        :param org_id: Optional target organization identifier, defaults to the token's org if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/actions/validate/invoke')
        super().post(url, params=params, json=body)

    def list_ai_receptionist_available_numbers(self, location_id: str, phone_number: str = None, org_id: str = None,
                                               **params: Any) -> Generator[AvailableNumber, None, None]:
        """
        List Available Numbers for AI Receptionist

        List and search numbers that can be assigned as AI Receptionist number.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Numbers
        listed here can be assigned to an AI receptionist at a location.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location ID.
        :type location_id: str
        :param phone_number: Search (Contains) based on number or extension. Search cannot be performed based on esn.
        :type phone_number: str
        :param org_id: Optional target organization identifier. Defaults to the token's org Id if not provided.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def get_ai_receptionist_voices(self, location_id: str, org_id: str = None) -> builtins.list[AiEngine]:
        """
        Get AI Receptionist Voices

        Get list of available AI Receptionist voices.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. This
        API returns the available voice options that can be configured for an AI Receptionist. The response returns
        all available engines and voices; no pagination is required.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location ID.
        :type location_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: list[AiEngine]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/voices')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AiEngine]).validate_python(data['aiEngines'])
        return r

    def delete_ai_receptionist(self, location_id: str, ai_receptionist_id: str, org_id: str = None) -> None:
        """
        Delete an AI Receptionist.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls to
        people or services.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}')
        super().delete(url, params=params)

    def get_ai_receptionist(self, location_id: str, ai_receptionist_id: str,
                            org_id: str = None) -> AiReceptionistResponse:
        """
        Get AI Receptionist details.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls to
        people or services.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`AiReceptionistResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}')
        data = super().get(url, params=params)
        r = AiReceptionistResponse.model_validate(data)
        return r

    def update_ai_receptionist(self, location_id: str, ai_receptionist_id: str, name: str = None, enabled: bool = None,
                               phone_number: str = None, extension: str = None,
                               alternate_numbers: list[UpdateAlternateNumber] = None,
                               direct_line_caller_id_name: DirectLineCallerIdName = None, dial_by_name: str = None,
                               default_action: UpdateDefaultAction = None, ai_agent: UpdateAiAgent = None,
                               org_id: str = None) -> None:
        """
        Update an AI Receptionist.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls to
        people or services.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param name: Name of the AI Receptionist. This has to be unique across location.
        :type name: str
        :param enabled: Flag to indicate AI receptionist is enabled or not. When disabled, incoming calls to this AI
            receptionist will not be answered.
        :type enabled: bool
        :param phone_number: Phone number of the AI Receptionist. Either phoneNumber or extension is mandatory. At
            least one is required.
        :type phone_number: str
        :param extension: Extension of the AI Receptionist. Either phoneNumber or extension is mandatory. At least one
            is required.
        :type extension: str
        :param alternate_numbers: List of alternate phone numbers to assign to the AI Receptionist.
        :type alternate_numbers: list[UpdateAlternateNumber]
        :param direct_line_caller_id_name: Direct line caller ID name configuration
        :type direct_line_caller_id_name: DirectLineCallerIdName
        :param dial_by_name: A dial by name used for AI Receptionist name dialing. Characters of `%`, `+`, `\\`, `"`
            and Unicode characters are not allowed.
        :type dial_by_name: str
        :param default_action: Default action configuration for the AI Receptionist
        :type default_action: UpdateDefaultAction
        :param ai_agent: AI Agent configuration
        :type ai_agent: UpdateAiAgent
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if name is not None:
            body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if alternate_numbers is not None:
            body['alternateNumbers'] = TypeAdapter(list[UpdateAlternateNumber]).dump_python(alternate_numbers, mode='json', by_alias=True, exclude_none=True)
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        if default_action is not None:
            body['defaultAction'] = default_action.model_dump(mode='json', by_alias=True, exclude_none=True)
        if ai_agent is not None:
            body['aiAgent'] = ai_agent.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}')
        super().put(url, params=params, json=body)

    def list_ai_receptionist_intents(self, location_id: str, ai_receptionist_id: str,
                                     org_id: str = None) -> builtins.list[AiReceptionistIntent]:
        """
        List AI Receptionist Intents

        Get list of AI Receptionist Intents.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Intents
        represent call-handling behaviors such as transfers.

        Returns all intents in a single response.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: list[AiReceptionistIntent]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}/intents')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AiReceptionistIntent]).validate_python(data['intents'])
        return r

    def create_ai_receptionist_intent(self, location_id: str, ai_receptionist_id: str, name: str, description: str,
                                      transfer_to: IntentTransferToRequest, org_id: str = None) -> str:
        """
        Create AI Receptionist Intent

        Create a new AI Receptionist Intent.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Intents
        represent call-handling behaviors such as transfers.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param name: Name of the intent.
        :type name: str
        :param description: Description of the intent (Action).
        :type description: str
        :param transfer_to: -
        :type transfer_to: IntentTransferToRequest
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        body['description'] = description
        body['transferTo'] = transfer_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}/intents')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_ai_receptionist_intent(self, location_id: str, ai_receptionist_id: str, intent_id: str,
                                      org_id: str = None) -> None:
        """
        Delete AI Receptionist Intent

        Delete an AI Receptionist Intent.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Intents
        represent call-handling behaviors such as transfers.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param intent_id: Unique identifier for a specific AI Receptionist intent within a given location and AI
            Receptionist instance.
        :type intent_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}/intents/{intent_id}')
        super().delete(url, params=params)

    def get_ai_receptionist_intent(self, location_id: str, ai_receptionist_id: str, intent_id: str,
                                   org_id: str = None) -> AiReceptionistIntentDetails:
        """
        Get AI Receptionist Intent

        Get details of a specific AI Receptionist Intent.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Intents
        represent call-handling behaviors such as transfers.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param intent_id: Unique identifier for a specific AI Receptionist intent within a given location and AI
            Receptionist instance.
        :type intent_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`AiReceptionistIntentDetails`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}/intents/{intent_id}')
        data = super().get(url, params=params)
        r = AiReceptionistIntentDetails.model_validate(data)
        return r

    def modify_ai_receptionist_intent(self, location_id: str, ai_receptionist_id: str, intent_id: str,
                                      name: str = None, description: str = None,
                                      transfer_to: IntentTransferToRequest = None, org_id: str = None) -> None:
        """
        Modify AI Receptionist Intent

        Modify an existing AI Receptionist Intent.

        AI Receptionist is a Webex Calling feature that uses AI to greet callers and intelligently route calls. Intents
        represent call-handling behaviors such as transfers.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location ID.
        :type location_id: str
        :param ai_receptionist_id: Unique identifier for the AI Receptionist.
        :type ai_receptionist_id: str
        :param intent_id: Unique identifier for a specific AI Receptionist intent within a given location and AI
            Receptionist instance.
        :type intent_id: str
        :param name: Name of the intent.
        :type name: str
        :param description: Description of the intent (Action).
        :type description: str
        :param transfer_to: -
        :type transfer_to: IntentTransferToRequest
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if transfer_to is not None:
            body['transferTo'] = transfer_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/locations/{location_id}/aiReceptionists/{ai_receptionist_id}/intents/{intent_id}')
        super().put(url, params=params, json=body)
