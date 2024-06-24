from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['RolesApi']

from wxc_sdk.common import IdAndName


class RolesApi(ApiChild, base='roles'):
    """
    Roles

    A persona for an authenticated user, corresponding to a set of privileges within an organization. This roles
    resource can be accessed only by an admin and shows only roles relevant to an admin.
    """

    def list(self) -> list[IdAndName]:
        """
        List Roles

        List all roles.

        :rtype: list[Role]
        """
        url = self.ep()
        data = super().get(url)
        r = TypeAdapter(list[IdAndName]).validate_python(data['items'])
        return r

    def details(self, role_id: str) -> IdAndName:
        """
        Get Role Details

        Shows details for a role, by ID.

        Specify the role ID in the `roleId` parameter in the URI.

        :param role_id: The unique identifier for the role.
        :type role_id: str
        :rtype: :class:`Role`
        """
        url = self.ep(f'{role_id}')
        data = super().get(url)
        r = IdAndName.model_validate(data)
        return r
