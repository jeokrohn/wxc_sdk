| Description                                               | Done | endpoint                                                                                                          |
|-----------------------------------------------------------|------|-------------------------------------------------------------------------------------------------------------------|
| Retrieve a person's Application Services Settings         | X    | GET https://webexapis.com/v1/people/{personId}/features/applications                                              |
| Modify a person's Application Services Settings           | X    | PUT https://webexapis.com/v1/people/{personId}/features/applications                                              |
| Read Barge In Settings for a Person                       | X    | GET https://webexapis.com/v1/people/{personId}/features/bargeIn                                                   |
| Configure Barge In Settings for a Person                  | X    | PUT https://webexapis.com/v1/people/{personId}/features/bargeIn                                                   |
| Read Forwarding Settings for a Person                     | X    | GET https://webexapis.com/v1/people/{personId}/features/callForwarding                                            |
| Configure Call Forwarding Settings for a Person           | X    | PUT https://webexapis.com/v1/people/{personId}/features/callForwarding                                            |
| Read Call Intercept Settings for a Person                 | X    | GET https://webexapis.com/v1/people/{personId}/features/intercept                                                 |
| Configure Call Intercept Settings for a Person            | X    | PUT https://webexapis.com/v1/people/{personId}/features/intercept                                                 |
| Configure Call Intercept Greeting for a Person            | X    | POST https://webexapis.com/v1/people/{personId}/features/intercept/actions/announcementUpload/invoke              |
| Read Call Recording Settings for a Person                 | X    | GET https://webexapis.com/v1/people/{personId}/features/callRecording                                             |
| Configure Call Recording Settings for a Person            | X    | PUT https://webexapis.com/v1/people/{personId}/features/callRecording                                             |
| Read Call Waiting Settings for a Person                   | X    | GET https://webexapis.com/v1/people/{personId}/features/callWaiting                                               |
| Configure Call Waiting Settings for a Person              | X    | PUT https://webexapis.com/v1/people/{personId}/features/callWaiting                                               |
| Read Caller ID Settings for a Person                      | X    | GET https://webexapis.com/v1/people/{personId}/features/callerId                                                  |
| Configure Caller ID Settings for a Person                 | X    | PUT https://webexapis.com/v1/people/{personId}/features/callerId                                                  |
| Read Person's Calling Behavior                            | X    | GET https://webexapis.com/v1/people/{personId}/features/callingBehavior                                           |
| Configure a person's Calling Behavior                     | X    | PUT https://webexapis.com/v1/people/{personId}/features/callingBehavior                                           |
| Read Do Not Disturb Settings for a Person                 | X    | GET https://webexapis.com/v1/people/{personId}/features/doNotDisturb                                              |
| Configure Do Not Disturb Settings for a Person            | X    | PUT https://webexapis.com/v1/people/{personId}/features/doNotDisturb                                              |
| Retrieve Executive Assistant Settings for a Person        | X    | GET https://webexapis.com/v1/people/{personId}/features/executiveAssistant                                        |
| Modify Executive Assistant Settings for a Person          | X    | PUT https://webexapis.com/v1/people/{personId}/features/executiveAssistant                                        |
| Read Hoteling Settings for a Person                       | X    | GET https://webexapis.com/v1/people/{personId}/features/hoteling                                                  |
| Configure Hoteling Settings for a Person                  | X    | PUT https://webexapis.com/v1/people/{personId}/features/hoteling                                                  |
| Retrieve a person's Monitoring Settings                   | X    | GET https://webexapis.com/v1/people/{personId}/features/monitoring                                                |
| Modify a person's Monitoring Settings                     | X    | PUT https://webexapis.com/v1/people/{personId}/features/monitoring                                                |
| Validate or Initiate Move Users Job                       | X    | POST https://webexapis.com/v1/telephony/config/jobs/person/moveLocation                                           |
| List Move Users Jobs                                      | X    | GET https://webexapis.com/v1/telephony/config/jobs/person/moveLocation                                            |
| Get Move Users Job Status                                 | X    | GET https://webexapis.com/v1/telephony/config/jobs/person/moveLocation/{jobId}                                    |
| Abandon the Move Users Job                                | X    | POST https://webexapis.com/v1/telephony/config/jobs/person/moveLocation/{jobId}/actions/abandon/invoke            |
| Pause the Move Users Job                                  | X    | POST https://webexapis.com/v1/telephony/config/jobs/person/moveLocation/{jobId}/actions/pause/invoke              |
| Resume the Move Users Job                                 | X    | POST https://webexapis.com/v1/telephony/config/jobs/person/moveLocation/{jobId}/actions/resume/invoke             |
| List Move Users Job errors                                | X    | GET https://webexapis.com/v1/telephony/config/jobs/person/moveLocation/{jobId}/errors                             |
| Retrieve Music On Hold Settings for a Person              | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/musicOnHold                                       |
| Configure Music On Hold Settings for a Person             | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/musicOnHold                                       |
| Read Incoming Permission Settings for a Person            | X    | GET https://webexapis.com/v1/people/{personId}/features/incomingPermission                                        |
| Configure Incoming Permission Settings for a Person       | X    | PUT https://webexapis.com/v1/people/{personId}/features/incomingPermission                                        |
| Retrieve a person's Outgoing Calling Permissions Settings | X    | GET https://webexapis.com/v1/people/{personId}/features/outgoingPermission                                        |
| Modify a person's Outgoing Calling Permissions Settings   | X    | PUT https://webexapis.com/v1/people/{personId}/features/outgoingPermission                                        |
| Get a List of Phone Numbers for a Person                  | X    | GET https://webexapis.com/v1/people/{personId}/features/numbers                                                   |
| Assign or Unassign numbers to a person                    | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/numbers                                           |
| Get Preferred Answer Endpoint                             | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/preferredAnswerEndpoint                           |
| Modify Preferred Answer Endpoint                          | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/preferredAnswerEndpoint                           |
| Get a person's Privacy Settings                           | X    | GET https://webexapis.com/v1/people/{personId}/features/privacy                                                   |
| Configure a person's Privacy Settings                     | X    | PUT https://webexapis.com/v1/people/{personId}/features/privacy                                                   |
| Read Push-to-Talk Settings for a Person                   | X    | GET https://webexapis.com/v1/people/{personId}/features/pushToTalk                                                |
| Configure Push-to-Talk Settings for a Person              | X    | PUT https://webexapis.com/v1/people/{personId}/features/pushToTalk                                                |
| Read Receptionist Client Settings for a Person            | X    | GET https://webexapis.com/v1/people/{personId}/features/reception                                                 |
| Configure Receptionist Client Settings for a Person       | X    | PUT https://webexapis.com/v1/people/{personId}/features/reception                                                 |
| List of Schedules for a Person                            | X    | GET https://webexapis.com/v1/people/{personId}/features/schedules                                                 |
| Create Schedule for a Person                              | X    | POST https://webexapis.com/v1/people/{personId}/features/schedules                                                |
| Get a Schedule Details                                    | X    | GET https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}                     |
| Update a Schedule                                         | X    | PUT https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}                     |
| Delete a Schedule                                         | X    | DELETE https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}                  |
| Fetch Event for a person's Schedule                       | X    | GET https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}/events/{eventId}    |
| Add a New Event for Person's Schedule                     | X    | POST https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}/events             |
| Update an Event for a person's Schedule                   | X    | PUT https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}/events/{eventId}    |
| Delete an Event for a person's Schedule                   | X    | DELETE https://webexapis.com/v1/people/{personId}/features/schedules/{scheduleType}/{scheduleId}/events/{eventId} |
| Search Shared-Line Appearance Members                     | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/applications/{applicationId}/availableMembers     |
| Get Shared-Line Appearance Members                        | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/applications/{applicationId}/members              |
| Put Shared-Line Appearance Members                        | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/applications/{applicationId}/members              |
| Read Voicemail Settings for a Person                      | X    | GET https://webexapis.com/v1/people/{personId}/features/voicemail                                                 |
| Configure Voicemail Settings for a Person                 | X    | PUT https://webexapis.com/v1/people/{personId}/features/voicemail                                                 |
| Configure Busy Voicemail Greeting for a Person            | X    | POST https://webexapis.com/v1/people/{personId}/features/voicemail/actions/uploadBusyGreeting/invoke              |
| Configure No Answer Voicemail Greeting for a Person       | X    | POST https://webexapis.com/v1/people/{personId}/features/voicemail/actions/uploadNoAnswerGreeting/invoke          |
| Reset Voicemail PIN                                       | X    | POST https://webexapis.com/v1/people/{personId}/features/voicemail/actions/resetPin/invoke                        |
| Get Message Summary                                       | X    | GET https://webexapis.com/v1/telephony/voiceMessages/summary                                                      |
| List Messages                                             | X    | GET https://webexapis.com/v1/telephony/voiceMessages                                                              |
| Delete Message                                            | X    | DELETE https://webexapis.com/v1/telephony/voiceMessages/{messageId}                                               |
| Mark As Read                                              | X    | POST https://webexapis.com/v1/telephony/voiceMessages/markAsRead                                                  |
| Mark As Unread                                            | X    | POST https://webexapis.com/v1/telephony/voiceMessages/markAsUnread                                                |
| Retrieve Agent's List of Available Caller IDs             | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/agent/availableCallerIds                          |
| Retrieve Agent's Caller ID Information                    | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/agent/callerId                                    |
| Modify Agent's Caller ID Information                      | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/agent/callerId                                    |
| Read Call Bridge Settings for a Person                    | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/features/callBridge                               |
| Configure Call Bridge Settings for a Person               | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/features/callBridge                               |
| Get Person Secondary Available Phone Numbers              | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/secondary/availableNumbers                        |
| Get Person Fax Message Available Phone Numbers            | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/faxMessage/availableNumbers                       |
| Get Person Call Forward Available Phone Numbers           | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/callForwarding/availableNumbers                   |
| Get Person Primary Available Phone Numbers                | X    | GET https://webexapis.com/v1/telephony/config/people/primary/availableNumbers                                     |
| Get Person ECBN Available Phone Numbers                   | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/emergencyCallbackNumber/availableNumbers          |
| Get Person Call Intercept Available Phone Numbers         | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/callIntercept/availableNumbers                    |
| Retrieve a Person's MS Teams Settings                     | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/settings/msTeams                                  |
| Configure a Person's MS Teams Setting                     | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/settings/msTeams                                  |
