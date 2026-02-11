#!/usr/bin/env bash
set -euo pipefail

export WEBEX_ACCESS_TOKEN="${WEBEX_ACCESS_TOKEN:?missing token}"

python actions/action_auto_attendant.py --mode apply --vars '{"aa_name": "AA-LAB-MADRID", "extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "schedule_name": "Horario-LAB-LV"}'
python actions/action_call_pickup_group.py --mode apply --vars '{"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "pickup_name": "PG-LAB-RECEPCION"}'
python actions/action_call_profiles.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA"}'
python actions/action_call_queue.py --mode apply --vars '{"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "queue_id": "MISSING_queue_id", "queue_name": "CQ-LAB-VENTAS"}'
python actions/action_day_t_numbers_caller_id.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "primary_number": "+34915559742549"}'
python actions/action_delegated_admin.py --mode apply --vars '{"principal_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "role_id": "Y2lzY29zcGFyazovL3VzL1JPTEUvaWRfdXNlcl9hZG1pbg", "scope": "organization"}'
python actions/action_devices.py --mode apply --vars '{"device_model": "Cisco 8851", "workspace_id": "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFLzQyOGI3NzVhLWYxNTgtNDVkOC1hOTJhLTg1OTllNTVjM2UxYw=="}'
python actions/action_group_assignment.py --mode apply --vars '{"group_id": "MISSING_group_id", "group_name": "LAB-GROUP-VOICE", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}'
python actions/action_hunt_group.py --mode apply --vars '{"extension": "5101", "hunt_name": "HG-LAB-SOPORTE", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}'
python actions/action_internal_extensions_sbc.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "route_group_id": "MISSING_route_group_id", "route_group_name": "RG-LAB-SBC", "trunk_id": "MISSING_trunk_id", "trunk_name": "TRUNK-LAB-MAIN"}'
python actions/action_interplatform_dial_plan.py --mode apply --vars '{"dial_pattern": "+3491XXXXXXX", "dial_plan_name": "DP-LAB-INTERPLATFORM", "route_group_id": "MISSING_route_group_id"}'
python actions/action_legacy_forwarding.py --mode apply --vars '{"forward_destination": "+34915550123", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}'
python actions/action_location_number_removal.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "primary_number": "+34915559742549"}'
python actions/action_manager_assistant.py --mode apply --vars '{"assistant_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MjYxMWNkMS1jMTJmLTQxNjgtODc1My04MDdmODJiOTYwNGQ", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}'
python actions/action_monitoring.py --mode apply --vars '{"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "target_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MjYxMWNkMS1jMTJmLTQxNjgtODc1My04MDdmODJiOTYwNGQ"}'
python actions/action_nominal_users.py --mode apply --vars '{"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "primary_number": "+34915559742549"}'
python actions/action_secondary_numbers.py --mode apply --vars '{"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "secondary_number": "+34915555861252"}'
python actions/action_user_recording.py --mode apply --vars '{"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}'
python actions/action_workspaces.py --mode apply --vars '{"extension": "5101", "primary_number": "+34915559742549", "workspace_id": "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFLzQyOGI3NzVhLWYxNTgtNDVkOC1hOTJhLTg1OTllNTVjM2UxYw=="}'
