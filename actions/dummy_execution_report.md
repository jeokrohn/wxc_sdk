# Dummy execution report

Base URL: `http://127.0.0.1:9` (sin backend, espera `connection refused`).

## action_auto_attendant.py
- command: `python actions\action_auto_attendant.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"aa_name": "AA-LAB-MADRID", "extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "schedule_name": "Horario-LAB-LV"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/autoAttendants (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001C38C92DF10>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:23,950 | INFO | action_auto_attendant | Completed action with 1 failure(s)`

## action_call_pickup_group.py
- command: `python actions\action_call_pickup_group.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx", "pickup_name": "PG-LAB-RECEPCION"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/callPickups (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000002A4418499D0>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:25,293 | INFO | action_call_pickup_group | Completed action with 1 failure(s)`

## action_call_profiles.py
- command: `python actions\action_call_profiles.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/callingBehavior (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000021C833816D0>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:26,649 | INFO | action_call_profiles | Completed action with 1 failure(s)`

## action_call_queue.py
- command: `python actions\action_call_queue.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx", "queue_id": "Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvUTE=", "queue_name": "CQ-LAB-VENTAS"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/queues (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001FF2650DF90>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:28,049 | INFO | action_call_queue | Completed action with 1 failure(s)`

## action_day_t_numbers_caller_id.py
- command: `python actions\action_day_t_numbers_caller_id.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "primary_number": "+34915550101"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/numbers (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000027DBCE1DD10>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:29,427 | INFO | action_day_t_numbers_caller_id | Completed action with 1 failure(s)`

## action_delegated_admin.py
- command: `python actions\action_delegated_admin.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"principal_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BRE1JTjE=", "role_id": "Y2lzY29zcGFyazovL3VzL1JPTEVTL1JPTEUx", "scope": "organization"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /roles (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000016948065A90>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:30,778 | INFO | action_delegated_admin | Completed action with 1 failure(s)`

## action_devices.py
- command: `python actions\action_devices.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"device_model": "Cisco 8851", "serial": "FTX1234LAB1", "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /devices?serial=FTX1234LAB1 (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000002050F7D5B10>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:32,209 | INFO | action_devices | Completed action with 1 failure(s)`

## action_group_assignment.py
- command: `python actions\action_group_assignment.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"group_id": "Y2lzY29zcGFyazovL3VzL0dST1VQUy9HUk9VUDE=", "group_name": "LAB-GROUP-VOICE", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /groups/Y2lzY29zcGFyazovL3VzL0dST1VQUy9HUk9VUDE=/members (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000011860B47590>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:34,678 | INFO | action_group_assignment | Completed action with 2 failure(s)`

## action_hunt_group.py
- command: `python actions\action_hunt_group.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "hunt_name": "HG-LAB-SOPORTE", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/huntGroups (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000014CCD9ADF50>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:36,137 | INFO | action_hunt_group | Completed action with 1 failure(s)`

## action_internal_extensions_sbc.py
- command: `python actions\action_internal_extensions_sbc.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ==", "route_group_name": "RG-LAB-SBC", "trunk_id": "Y2lzY29zcGFyazovL3VzL1RSVU5LUy9UUlVOSzE=", "trunk_name": "TRUNK-LAB-MAIN"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/premisePstn/routeGroups/Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ== (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001F7F3CFB310>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:38,559 | INFO | action_internal_extensions_sbc | Completed action with 2 failure(s)`

## action_interplatform_dial_plan.py
- command: `python actions\action_interplatform_dial_plan.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"dial_pattern": "+3491XXXXXXX", "dial_plan_name": "DP-LAB-INTERPLATFORM", "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/dialPlans (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000024C95B073D0>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:40,944 | INFO | action_interplatform_dial_plan | Completed action with 2 failure(s)`

## action_legacy_forwarding.py
- command: `python actions\action_legacy_forwarding.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"forward_destination": "+34915550123", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/callForwarding (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000022E75AF57D0>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:42,363 | INFO | action_legacy_forwarding | Completed action with 1 failure(s)`

## action_location_number_removal.py
- command: `python actions\action_location_number_removal.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "primary_number": "+34915550101"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/numbers (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000002B41E755610>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:43,769 | INFO | action_location_number_removal | Completed action with 1 failure(s)`

## action_manager_assistant.py
- command: `python actions\action_manager_assistant.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"assistant_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BU1NJU1RBTlQx", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/executiveAssistant (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000020A24C75750>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:45,148 | INFO | action_manager_assistant | Completed action with 1 failure(s)`

## action_monitoring.py
- command: `python actions\action_monitoring.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "target_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9UQVJHRVQx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/monitoring (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001CDF29E8A10>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:46,572 | INFO | action_monitoring | Completed action with 1 failure(s)`

## action_nominal_users.py
- command: `python actions\action_nominal_users.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"email": "dummy.user.lab@lab.example.com", "extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "primary_number": "+34915550101"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/numbers (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001D00B363250>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:48,928 | INFO | action_nominal_users | Completed action with 2 failure(s)`

## action_secondary_numbers.py
- command: `python actions\action_secondary_numbers.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "secondary_number": "+34915550222"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/numbers (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000011FB9A29990>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:50,309 | INFO | action_secondary_numbers | Completed action with 1 failure(s)`

## action_user_recording.py
- command: `python actions\action_user_recording.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/callRecording (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x00000212191E5750>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:51,682 | INFO | action_user_recording | Completed action with 1 failure(s)`

## action_workspaces.py
- command: `python actions\action_workspaces.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "primary_number": "+34915550101", "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx", "workspace_name": "WS-LAB-REUNIONES"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/workspaces/Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx/numbers (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x0000023E2B04B3D0>, 'Connection to 127.0.0.1 timed out. (connect timeout=1)'))`
  - `2026-02-08 11:57:54,036 | INFO | action_workspaces | Completed action with 2 failure(s)`
