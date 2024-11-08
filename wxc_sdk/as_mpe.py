from aiohttp import FormData

__all__ = ['MultipartEncoder']


class MultipartEncoder(FormData):
    """
    Compatibility class for requests toolbelt MultipartEncoder
    """

    def __init__(self, body):
        super().__init__()
        for name, value in body.items():
            if isinstance(value, str):
                self.add_field(name, value)
            elif isinstance(value, tuple):
                self.add_field(name, value=value[1], content_type=value[2], filename=value[0])
            else:
                raise NotImplementedError

    @property
    def content_type(self) -> str:
        return self._writer.content_type
