| Description                                                | Done | endpoint                                                                                               |
|------------------------------------------------------------|------|--------------------------------------------------------------------------------------------------------|
| Get Device Members                                         | X    | GET https://webexapis.com/v1/telephony/config/devices/{deviceId}/members                               |
| Update Members on the device                               | X    | PUT https://webexapis.com/v1/telephony/config/devices/{deviceId}/members                               |
| Search Members                                             | X    | GET https://webexapis.com/v1/telephony/config/devices/{deviceId}/availableMembers                      |
| Apply Changes for a specific device                        | X    | POST https://webexapis.com/v1/telephony/config/devices/{deviceId}/actions/applyChanges/invoke          |
| Get Device Settings                                        | X    | GET https://webexapis.com/v1/telephony/config/devices/{deviceId}/settings                              |
| Update device settings                                     | X    | PUT https://webexapis.com/v1/telephony/config/devices/{deviceId}/settings                              |
| Get Location Device Settings                               | X    | GET https://webexapis.com/v1/telephony/config/locations/{locationId}/devices/settings                  |
| Get Webex Calling Device Details                           | X    | GET https://webexapis.com/v1/telephony/config/devices/{deviceId}                                       |
| Update Third Party Device                                  | X    | PUT https://webexapis.com/v1/telephony/config/devices/{deviceId}                                       |
| Get Person Devices                                         | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/devices                                |
| Modify Hoteling Settings for a Person's Primary Devices    | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/devices/settings/hoteling              |
| Get Workspace Devices                                      | X    | GET https://webexapis.com/v1/telephony/config/workspaces/{workspaceId}/devices                         |
| Modify Workspace Devices                                   | X    | PUT https://webexapis.com/v1/telephony/config/workspaces/{workspaceId}/devices                         |
| Read the List of Supported Devices                         | X    | GET https://webexapis.com/v1/telephony/config/supportedDevices                                         |
| Read the device override settings for a organization       | X    | GET https://webexapis.com/v1/telephony/config/devices/settings                                         |
| Create a Line Key Template                                 | X    | POST https://webexapis.com/v1/telephony/config/devices/lineKeyTemplates                                |
| Read the list of Line Key Templates                        | X    | GET https://webexapis.com/v1/telephony/config/devices/lineKeyTemplates                                 |
| Get details of a Line Key Template                         | X    | GET https://webexapis.com/v1/telephony/config/devices/lineKeyTemplates/{templateId}                    |
| Modify a Line Key Template                                 | X    | PUT https://webexapis.com/v1/telephony/config/devices/lineKeyTemplates/{templateId}                    |
| Delete a Line Key Template                                 | X    | DELETE https://webexapis.com/v1/telephony/config/devices/lineKeyTemplates/{templateId}                 |
| Preview Apply Line Key Template                            | X    | POST https://webexapis.com/v1/telephony/config/devices/actions/previewApplyLineKeyTemplate/invoke      |
| Apply a Line key Template                                  | X    | POST https://webexapis.com/v1/telephony/config/jobs/devices/applyLineKeyTemplate                       |
| Get List of Apply Line Key Template jobs                   | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/applyLineKeyTemplate                        |
| Get the job status of an Apply Line Key Template job       | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/applyLineKeyTemplate/{jobId}                |
| Get job errors for an Apply Line Key Template job          | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/applyLineKeyTemplate/{jobId}/errors         |
| Read the DECT device type list - Deprecated                | X    | GET https://webexapis.com/v1/telephony/config/devices/dects/supportedDevices                           |
| Read the DECT device type list                             | X    | GET https://webexapis.com/v1/telephony/config/devices/dectNetworks/supportedDevices                    |
| Validate a list of MAC address                             | X    | POST https://webexapis.com/v1/telephony/config/devices/actions/validateMacs/invoke                     |
| Change Device Settings Across Organization Or Location Job | X    | POST https://webexapis.com/v1/telephony/config/jobs/devices/callDeviceSettings                         |
| List Change Device Settings Jobs                           | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/callDeviceSettings                          |
| Get Change Device Settings Job Status                      | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/callDeviceSettings/{jobId}                  |
| List Change Device Settings Job Errors                     | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/callDeviceSettings/{jobId}/errors           |
| Get Device Layout by Device ID                             | X    | GET https://webexapis.com/v1/telephony/config/devices/{deviceId}/layout                                |
| Modify Device Layout by Device ID                          | X    | PUT https://webexapis.com/v1/telephony/config/devices/{deviceId}/layout                                |
| Rebuild Phones Configuration                               | X    | POST https://webexapis.com/v1/telephony/config/jobs/devices/rebuildPhones                              |
| List Rebuild Phones Jobs                                   | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/rebuildPhones                               |
| Get the Job Status of a Rebuild Phones Job                 | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/rebuildPhones/{jobId}                       |
| Get Job Errors for a Rebuild Phones Job                    | X    | GET https://webexapis.com/v1/telephony/config/jobs/devices/rebuildPhones/{jobId}/errors                |
| Get Device Settings for a Person                           | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/devices/settings                       |
| Update Device Settings for a Person                        | X    | PUT https://webexapis.com/v1/telephony/config/people/{personId}/devices/settings                       |
| Get Device Settings for a Workspace                        | X    | GET https://webexapis.com/v1/telephony/config/workspaces/{workspaceId}/devices/settings                |
| Update Device Settings for a Workspace                     | X    | PUT https://webexapis.com/v1/telephony/config/workspaces/{workspaceId}/devices/settings                |
| Read the List of Background Images                         | X    | GET https://webexapis.com/v1/telephony/config/devices/backgroundImages                                 |
| Upload a Device Background Image                           | X    | POST https://webexapis.com/v1/telephony/config/devices/{deviceId}/actions/backgroundImageUpload/invoke |
| Delete Device Background Images                            | X    | DELETE https://webexapis.com/v1/telephony/config/devices/backgroundImages                              |
| Get User Devices Count                                     | X    | GET https://webexapis.com/v1/telephony/config/people/{personId}/devices/count                          |
