import time
from collections.abc import Callable

from tests.base import TestCaseWithUsers
from wxc_sdk.people import Person
from wxc_sdk.person_settings import DeviceActivationState, TelephonyDevice
from wxc_sdk.person_settings.preferred_answer import (
    PreferredAnswerEndpoint,
    PreferredAnswerEndpointType,
    PreferredAnswerResponse,
)
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.calls import CallState, TelephonyCall


class TestCallControlsMembers(TestCaseWithUsers):
    """
    Integration tests for Webex Calling member-level call control operations.

    This test class validates an end-to-end call flow using the
    `api.telephony.call_controls_members` API:
    1. Resolve target users by display name.
    2. Discover preferred-answer endpoints for each user.
    3. Ensure each user has exactly one "registered" device for this scenario.
    4. Place a call from Heidi to Ken.
    5. Answer on Ken's endpoint and verify both legs are connected.
    6. Clean up active calls at the end of the test.
    """

    #: Time (in seconds) between polling attempts in `wait_for_call`.
    poll_interval = 2.0
    #: Maximum wait time (in seconds) for a call state transition.
    poll_timeout = 45.0

    def target_user(self, display_name: str) -> Person:
        """
        Find a calling-enabled user by display name.

        The lookup first uses `self.users` (loaded by `TestCaseWithUsers`)
        If no user is found, the test is skipped.

        :param display_name: Full display name to search for.
        :return: Person details with `calling_data=True`.
        """
        user = next((user for user in self.users if user.display_name == display_name), None)
        if user is None:
            self.skipTest(f'No calling user named {display_name!r}')
        return self.api.people.details(user.person_id, calling_data=True)

    def preferred_answer(self, user: Person) -> PreferredAnswerResponse:
        """
        Retrieve and print preferred-answer endpoint information for a user.

        Preferred-answer endpoints are valid endpoint IDs that can be used for
        call control actions such as dial/answer.

        :param user: Target user.
        :return: Preferred-answer settings response.
        """
        preferred_answer = self.api.person_settings.preferred_answer.read(user.person_id)
        print(f'{user.display_name} preferred answer endpoints:')
        for endpoint in preferred_answer.endpoints:
            selected = endpoint.id == preferred_answer.preferred_answer_endpoint_id and ' [preferred]' or ''
            print(f'  - {endpoint.type}: {endpoint.name} ({endpoint.id}){selected}')
        return preferred_answer

    def registered_devices(self, user: Person) -> list[TelephonyDevice]:
        """
        Return devices that qualify as "registered" for this test.

        A device is included only when all of the following are true:
        - Person settings show `activation_state == activated`.
        - Device details from `api.devices.details()` show
          `connection_status == connected`.

        This matches the requirement to consider only devices currently connected
        in the core devices API.

        :param user: Target user.
        :return: Filtered list of qualifying telephony devices.
        """
        from wxc_sdk.devices import ConnectionStatus

        devices = self.api.person_settings.devices(user.person_id).devices
        result = []
        for device in devices:
            print(
                f'{user.display_name} device: {device.model}, activation={device.activation_state}, '
                f'primary_owner={device.primary_owner}, mac={device.mac or "n/a"}'
            )
            # Filter out non-activated telephony devices.
            if device.activation_state != DeviceActivationState.activated:
                continue
            # Validate real-time connection state via Devices API.
            try:
                general_device = self.api.devices.details(device.device_id)
                if general_device.connection_status == ConnectionStatus.connected:
                    result.append(device)
                else:
                    print(f'  -> Skipping {device.model}: connection_status={general_device.connection_status}')
            except Exception as e:
                # Keep test running; missing/failed details are treated as non-registered.
                print(f'  -> Failed to get device details for {device.device_id}: {e}')
        return result

    def single_registered_device_endpoint(self, user: Person) -> PreferredAnswerEndpoint:
        """
        Resolve the single DEVICE preferred-answer endpoint for a user's registered device.

        Preconditions:
        - Exactly one registered device must exist (from `registered_devices`).
        - A DEVICE-type preferred-answer endpoint must match that device.

        :param user: Target user.
        :return: Matching preferred-answer endpoint.
        :raises AssertionError: If constraints are not met.
        """
        preferred_answer = self.preferred_answer(user)
        device_endpoints = [
            endpoint for endpoint in preferred_answer.endpoints if endpoint.type == PreferredAnswerEndpointType.device
        ]
        registered_devices = self.registered_devices(user)

        self.assertEqual(
            1,
            len(registered_devices),
            f'{user.display_name} must have exactly one registered device; found {len(registered_devices)}',
        )

        # Try to match the single registered device to a DEVICE endpoint.
        device_endpoint = next(
            (endpoint for endpoint in device_endpoints if endpoint.id == registered_devices[0].device_id),
            None,
        )
        if device_endpoint is None:
            self.fail(
                f'{user.display_name} has {len(registered_devices)} registered device(s) but no matching DEVICE '
                f'preferred-answer endpoint; '
                f'found {len(device_endpoints)} DEVICE endpoint(s)'
            )
        return device_endpoint

    def wait_for_call(
        self,
        member_id: str,
        *,
        description: str,
        predicate: Callable[[TelephonyCall], bool],
        timeout: float = None,
    ) -> TelephonyCall:
        """
        Poll active calls for a member until a call matches the predicate.

        :param member_id: Member ID (person/workspace/virtual line) for call lookup.
        :param description: Human-readable wait condition used in timeout failure text.
        :param predicate: Function that returns True for the desired call.
        :param timeout: Optional per-call timeout; defaults to `self.poll_timeout`.
        :return: The first matching call.
        :raises AssertionError: If timeout is reached.
        """
        timeout = timeout or self.poll_timeout
        deadline = time.monotonic() + timeout
        calls_api = self.api.telephony.call_controls_members
        last_calls: list[TelephonyCall] = []

        while time.monotonic() < deadline:
            last_calls = calls_api.list_calls(member_id=member_id)
            match = next((call for call in last_calls if predicate(call)), None)
            if match is not None:
                return match
            time.sleep(self.poll_interval)

        def render(call: TelephonyCall) -> str:
            """Format active call details for timeout diagnostics."""
            remote = call.remote_party.name or call.remote_party.number
            return (
                f'call_id={call.call_id}, session={call.call_session_id}, state={call.state}, '
                f'personality={call.personality}, remote={remote}'
            )

        active_calls = ', '.join(render(call) for call in last_calls) or 'none'
        self.fail(f'Timeout waiting for {description}. Active calls for member {member_id}: {active_calls}')

    def test_heidi_calls_ken(self):
        """
        Validate call flow where Heidi calls Ken (extension 7108) using member call controls.

        Flow:
        1. Resolve Heidi and Ken users.
        2. Assert Ken extension is 7108.
        3. Resolve each user's eligible endpoint.
        4. Dial Ken from Heidi.
        5. Wait for Ken to alert and answer on Ken's endpoint.
        6. Assert both call legs become connected.
        7. Always attempt hangup cleanup for both members.
        """
        calls_api = self.api.telephony.call_controls_members
        heidi = self.target_user('Heidi Harper')
        ken = self.target_user('Ken Alvarez')

        self.assertEqual('7108', ken.extension, f'Expected Ken Alvarez to have extension 7108, found {ken.extension!r}')

        heidi_endpoint = self.single_registered_device_endpoint(heidi)
        ken_endpoint = self.single_registered_device_endpoint(ken)

        heidi_call_id = None
        ken_call_id = None

        # Start the outbound call from Heidi to Ken's extension.
        dial = calls_api.dial(member_id=heidi.person_id, destination=ken.extension, endpoint_id=heidi_endpoint.id)
        heidi_call_id = dial.call_id
        print(
            f'Initiated click-to-dial from {heidi.display_name} to {ken.display_name} ({ken.extension}); '
            f'call_id={dial.call_id}, call_session_id={dial.call_session_id}'
        )

        try:
            # Wait for Heidi's call leg to appear in the expected call session.
            heidi_call = self.wait_for_call(
                heidi.person_id,
                description=f'{heidi.display_name} click-to-dial call {dial.call_id}',
                predicate=lambda call: call.call_session_id == dial.call_session_id,
            )
            heidi_call_id = heidi_call.call_id
            print(
                f'{heidi.display_name} call state after dial: state={heidi_call.state}, '
                f'personality={heidi_call.personality}, remote={heidi_call.remote_party.number}'
            )

            # Wait for Ken's leg to alert.
            ken_call = self.wait_for_call(
                ken.person_id,
                description=f'{ken.display_name} incoming call from {heidi.display_name}',
                predicate=lambda call: (
                    call.call_session_id == dial.call_session_id and call.state == CallState.alerting
                ),
            )
            ken_call_id = ken_call.call_id
            print(
                f'{ken.display_name} has incoming call: state={ken_call.state}, '
                f'remote={ken_call.remote_party.name or ken_call.remote_party.number}'
            )

            # Answer Ken's incoming call on his resolved endpoint.
            print(f'Answering {ken.display_name} on endpoint {ken_endpoint.name}')
            calls_api.answer(member_id=ken.person_id, call_id=ken_call.call_id, endpoint_id=ken_endpoint.id)

            # Confirm both call legs reach connected state in the same session.
            heidi_connected = self.wait_for_call(
                heidi.person_id,
                description=f'{heidi.display_name} connected call to {ken.display_name}',
                predicate=lambda call: (
                    call.call_session_id == dial.call_session_id and call.state == CallState.connected
                ),
            )
            ken_connected = self.wait_for_call(
                ken.person_id,
                description=f'{ken.display_name} connected call from {heidi.display_name}',
                predicate=lambda call: (
                    call.call_session_id == dial.call_session_id and call.state == CallState.connected
                ),
            )
            heidi_call_id = heidi_connected.call_id
            ken_call_id = ken_connected.call_id

            self.assertEqual(CallState.connected, heidi_connected.state)
            self.assertEqual(CallState.connected, ken_connected.state)
            self.assertEqual(dial.call_session_id, heidi_connected.call_session_id)
            self.assertEqual(dial.call_session_id, ken_connected.call_session_id)
        finally:
            # Cleanup both sides; ignore "Call not found" because one side may already be released.
            for member, call_id in ((ken, ken_call_id), (heidi, heidi_call_id)):
                if call_id is None:
                    continue
                try:
                    print(f'Hanging up call {call_id} for {member.display_name}')
                    calls_api.hangup(member_id=member.person_id, call_id=call_id)
                except Exception as e:
                    e: RestError
                    if e.description == 'Call not found':
                        continue
                    print(f'Failed to hang up call {call_id} for {member.display_name}: {e}')
        return
