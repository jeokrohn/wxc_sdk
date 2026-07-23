"""
Regression tests for the internal OpenAPI document models.
"""

from open_api.open_api_model import OASpec


def test_schema_property_parses_multiple_of_keyword() -> None:
    """
    Parse and preserve an OpenAPI ``multipleOf`` schema constraint.

    :return: None.
    :rtype: None
    """
    spec = OASpec.model_validate(
        {
            'openapi': '3.0.3',
            'info': {
                'title': 'Multiple-of regression',
                'version': '1.0.0',
                'description': 'Minimal OpenAPI document for parser regression coverage.',
            },
            'paths': {},
            'components': {
                'schemas': {
                    'Repeat': {
                        'type': 'object',
                        'properties': {
                            'interval': {
                                'type': 'integer',
                                'minimum': 10,
                                'maximum': 80,
                                'multipleOf': 10,
                            }
                        },
                    }
                }
            },
        }
    )

    interval = spec.components.schemas['Repeat'].properties['interval']

    assert interval.multiple_of == 10
    assert interval.model_dump(by_alias=True, exclude_none=True)['multipleOf'] == 10
