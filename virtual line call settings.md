| Description                                                     | Done | endpoint                                                                                                                |
|-----------------------------------------------------------------|------|-------------------------------------------------------------------------------------------------------------------------|
| Read the List of Virtual Lines                                  | X    | GET https://webexapis.com/v1/telephony/config/virtualLines                                                                  |
| Read Call Recording Settings for a Virtual Line                 | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callRecording                                    |
| Configure Call Recording Settings for a Virtual Line            | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callRecording                                    |
| Create a Virtual Line                                           | X    | POST https://webexapis.com/v1/telephony/config/virtualLines                                                                 |
| Delete a Virtual Line                                           | X    | DELETE https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}                                               |
| GET Details for a Virtual Line                                  | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}                                                  |
| Update a Virtual Line                                           | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}                                                  |
| GET Phone Number assigned for a Virtual Line                    | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/number                                           |
| Update Directory search for a Virtual Line                      | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/directorySearch                                  |
| GET List of Devices assigned for a Virtual Line                 | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/devices                                          |
| GET List of DECT Networks Handsets for a Virtual Line           | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/dectNetworks                                     |
| Read Caller ID Settings for a Virtual Line                      | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callerId                                         |
| Configure Caller ID Settings for a Virtual Line                 | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callerId                                         |
| Read Call Waiting Settings for a Virtual Line                   | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callWaiting                                      |
| Configure Call Waiting Settings for a Virtual Line              | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callWaiting                                      |
| Read Call Forwarding Settings for a Virtual Line                | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callForwarding                                   |
| Configure Call Forwarding Settings for a Virtual Line           | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callForwarding                                   |
| Read Incoming Permission Settings for a Virtual Line            | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/incomingPermission                               |
| Configure Incoming Permission Settings for a Virtual Line       | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/incomingPermission                               |
| Retrieve a virtual line's Outgoing Calling Permissions Settings | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/outgoingPermission                               |
| Modify a virtual line's Outgoing Calling Permissions Settings   | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/outgoingPermission                               |
| Read Call Intercept Settings for a Virtual Line                 | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/intercept                                        |
| Configure Call Intercept Settings for a Virtual Line            | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/intercept                                        |
| Configure Call Intercept Greeting for a Virtual Line            | X    | POST https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/intercept/actions/announcementUpload/invoke     |
| Retrieve Agent's List of Available Caller IDs                   | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/agent/availableCallerIds                         |
| Retrieve Agent's Caller ID Information                          | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/agent/callerId                                   |
| Modify Agent's Caller ID Information                            | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/agent/callerId                                   |
| Read Voicemail Settings for a Virtual Line                      | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/voicemail                                        |
| Configure Voicemail Settings for a Virtual Line                 | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/voicemail                                        |
| Configure Busy Voicemail Greeting for a Virtual Line            | X    | POST https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/voicemail/actions/uploadBusyGreeting/invoke     |
| Configure No Answer Voicemail Greeting for a Virtual Line       | X    | POST https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/voicemail/actions/uploadNoAnswerGreeting/invoke |
| Reset Voicemail PIN for a Virtual Line                          | X    | POST https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/voicemail/actions/resetPin/invoke               |
| Retrieve Music On Hold Settings for a Virtual Line              | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/musicOnHold                                      |
| Configure Music On Hold Settings for a Virtual Line             | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/musicOnHold                                      |
| Read Push-to-Talk Settings for a Virtual Line                   | x    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/pushToTalk                                       |
| Configure Push-to-Talk Settings for a Virtual Line              | x    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/pushToTalk                                       |
| Read Call Bridge Settings for a Virtual Line                    | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callBridge                                       |
| Configure Call Bridge Settings for a Virtual Line               | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callBridge                                       |
| Read Barge In Settings for a Virtual Line                       | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/bargeIn                                          |
| Configure Barge In Settings for a Virtual Line                  | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/bargeIn                                          |
| GET a Virtual Line's Privacy Settings                           | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/privacy                                          |
| Configure a Virtual Line's Privacy Settings                     | X    | PUT https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/privacy                                          |
| GET Virtual Line Fax Message Available Phone Numbers            | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/faxMessage/availableNumbers                      |
| GET Virtual Line Call Forward Available Phone Numbers           | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/callForwarding/availableNumbers                  |
| GET Virtual Line Available Phone Numbers                        | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/availableNumbers                                                 |
| GET Virtual Line ECBN Available Phone Numbers                   | X    | GET https://webexapis.com/v1/telephony/config/virtualLines/{virtualLineId}/emergencyCallbackNumber/availableNumbers         |