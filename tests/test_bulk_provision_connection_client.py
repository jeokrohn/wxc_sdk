import responses

from wxc_sdk.bulk_provision.connection_client import ConnectionClient


@responses.activate
def test_connection_client_request_success() -> None:
    responses.add(
        responses.GET,
        "https://webexapis.com/v1/test",
        json={"ok": True},
        status=200,
    )
    client = ConnectionClient(
        base_url="https://webexapis.com/v1",
        token="token",
        timeout_seconds=5,
        max_retries=2,
        verify=True,
    )
    result = client.request("GET", "test")
    assert result.data["ok"] is True
