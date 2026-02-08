# Dummy execution report

Base URL: `http://127.0.0.1:9` (sin backend, espera `connection refused`).

## action_auto_attendant.py
- command: `python actions/action_auto_attendant.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"aa_name": "AA-LAB-MADRID", "extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "schedule_name": "Horario-LAB-LV"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/autoAttendants (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:54,325 | INFO | action_auto_attendant | Completed action with 1 failure(s)`

## action_call_pickup_group.py
- command: `python actions/action_call_pickup_group.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx", "pickup_name": "PG-LAB-RECEPCION"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/callPickups (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:54,556 | INFO | action_call_pickup_group | Completed action with 1 failure(s)`

## action_call_profiles.py
- command: `python actions/action_call_profiles.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/callingBehavior (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:54,747 | INFO | action_call_profiles | Completed action with 1 failure(s)`

## action_call_queue.py
- command: `python actions/action_call_queue.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx", "queue_id": "Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvUTE=", "queue_name": "CQ-LAB-VENTAS"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/queues (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:54,937 | INFO | action_call_queue | Completed action with 1 failure(s)`

## action_day_t_numbers_caller_id.py
- command: `python actions/action_day_t_numbers_caller_id.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "primary_number": "+34915550101"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/numbers (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:55,136 | INFO | action_day_t_numbers_caller_id | Completed action with 1 failure(s)`

## action_delegated_admin.py
- command: `python actions/action_delegated_admin.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"principal_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BRE1JTjE=", "role_id": "Y2lzY29zcGFyazovL3VzL1JPTEVTL1JPTEUx", "scope": "organization"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /roles (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:55,329 | INFO | action_delegated_admin | Completed action with 1 failure(s)`

## action_devices.py
- command: `python actions/action_devices.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"device_model": "Cisco 8851", "serial": "FTX1234LAB1", "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /devices?serial=FTX1234LAB1 (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:55,524 | INFO | action_devices | Completed action with 1 failure(s)`

## action_group_assignment.py
- command: `python actions/action_group_assignment.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"group_id": "Y2lzY29zcGFyazovL3VzL0dST1VQUy9HUk9VUDE=", "group_name": "LAB-GROUP-VOICE", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /groups/Y2lzY29zcGFyazovL3VzL0dST1VQUy9HUk9VUDE=/members (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:55,729 | INFO | action_group_assignment | Completed action with 2 failure(s)`

## action_hunt_group.py
- command: `python actions/action_hunt_group.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "hunt_name": "HG-LAB-SOPORTE", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/huntGroups (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:55,935 | INFO | action_hunt_group | Completed action with 1 failure(s)`

## action_internal_extensions_sbc.py
- command: `python actions/action_internal_extensions_sbc.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ==", "route_group_name": "RG-LAB-SBC", "trunk_id": "Y2lzY29zcGFyazovL3VzL1RSVU5LUy9UUlVOSzE=", "trunk_name": "TRUNK-LAB-MAIN"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/premisePstn/routeGroups/Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ== (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:56,129 | INFO | action_internal_extensions_sbc | Completed action with 2 failure(s)`

## action_interplatform_dial_plan.py
- command: `python actions/action_interplatform_dial_plan.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"dial_pattern": "+3491XXXXXXX", "dial_plan_name": "DP-LAB-INTERPLATFORM", "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/dialPlans (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:56,339 | INFO | action_interplatform_dial_plan | Completed action with 2 failure(s)`

## action_legacy_forwarding.py
- command: `python actions/action_legacy_forwarding.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"forward_destination": "+34915550123", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/callForwarding (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:56,548 | INFO | action_legacy_forwarding | Completed action with 1 failure(s)`

## action_location_number_removal.py
- command: `python actions/action_location_number_removal.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "primary_number": "+34915550101"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=/numbers (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:56,753 | INFO | action_location_number_removal | Completed action with 1 failure(s)`

## action_manager_assistant.py
- command: `python actions/action_manager_assistant.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"assistant_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BU1NJU1RBTlQx", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/executiveAssistant (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:56,954 | INFO | action_manager_assistant | Completed action with 1 failure(s)`

## action_monitoring.py
- command: `python actions/action_monitoring.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "target_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9UQVJHRVQx"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/monitoring (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:57,154 | INFO | action_monitoring | Completed action with 1 failure(s)`

## action_nominal_users.py
- command: `python actions/action_nominal_users.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"email": "dummy.user.lab@lab.example.com", "extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "primary_number": "+34915550101"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/numbers (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:57,351 | INFO | action_nominal_users | Completed action with 2 failure(s)`

## action_secondary_numbers.py
- command: `python actions/action_secondary_numbers.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "secondary_number": "+34915550222"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/numbers (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:57,554 | INFO | action_secondary_numbers | Completed action with 1 failure(s)`

## action_user_recording.py
- command: `python actions/action_user_recording.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/people/Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==/callRecording (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:57,753 | INFO | action_user_recording | Completed action with 1 failure(s)`

## action_workspaces.py
- command: `python actions/action_workspaces.py --mode probe --base-url http://127.0.0.1:9 --token DUMMY_TOKEN --timeout 1 --retries 1 --vars {"extension": "5101", "primary_number": "+34915550101", "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx", "workspace_name": "WS-LAB-REUNIONES"}`
- exit_code: `1` (OK)
- stderr_tail:
  - `requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /telephony/config/workspaces/Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx/numbers (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [Errno 111] Connection refused"))`
  - `2026-02-08 10:00:57,967 | INFO | action_workspaces | Completed action with 2 failure(s)`
