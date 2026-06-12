"""Tests for legacy dispatch and generated-source model matching."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from script import find_equivalent_models as cli
from script import generated_model_equivalents as fem


# Fixture helpers keep generated and SDK source snippets small and readable.
def write_py(path: Path, source: str) -> Path:
    """Write a dedented Python source fixture.

    :param path: File path to write.
    :type path: Path
    :param source: Python source text.
    :type source: str
    :return: Written file path.
    :rtype: Path
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(source))
    return path


def analyze(tmp_path: Path, generated_source: str, sdk_sources: dict[str, str]) -> fem.GeneratedAnalysisResult:
    """Build temporary generated and SDK files, then analyze them.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :param generated_source: Generated Python source fixture.
    :type generated_source: str
    :param sdk_sources: Mapping of SDK-relative paths to source fixtures.
    :type sdk_sources: dict[str, str]
    :return: Generated-file analysis result.
    :rtype: fem.GeneratedAnalysisResult
    """
    generated_file = write_py(
        tmp_path / 'open_api' / 'generated' / 'feature_auto.py',
        generated_source,
    )
    sdk_root = tmp_path / 'wxc_sdk'
    for rel_path, source in sdk_sources.items():
        write_py(sdk_root / rel_path, source)
    return fem.analyse_generated_file(generated_file=generated_file, sdk_root=sdk_root)


def matches_by_generated_name(result: fem.GeneratedAnalysisResult) -> dict[str, fem.GeneratedModelMatch]:
    """Index generated model matches by generated class name.

    :param result: Generated-file analysis result.
    :type result: fem.GeneratedAnalysisResult
    :return: Mapping from generated model name to match result.
    :rtype: dict[str, fem.GeneratedModelMatch]
    """
    return {match.generated.name: match for match in result.matches}


# CLI dispatch tests protect the restored legacy no-argument behavior.
def test_no_generated_file_selects_legacy_mode() -> None:
    """Verify that omitting the generated file selects legacy defaults.

    :return: ``None``.
    :rtype: None
    """
    args = cli.parse_args([])

    assert args.generated_file is None
    assert args.max_diff == 3
    assert args.min_fields == 3


def test_generated_only_flags_require_generated_file() -> None:
    """Verify generated-only options fail in legacy no-file mode.

    :return: ``None``.
    :rtype: None
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['--added-only'])


# Generated-mode tests exercise structural matching without importing fixtures.
def test_exact_field_name_match(tmp_path: Path) -> None:
    """Verify SDK models with identical field names are exact matches.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
            beta: int
        """,
        {
            '__init__.py': """
                from wxc_sdk.base import ApiModel


                class ExistingThing(ApiModel):
                    beta: int
                    alpha: str
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'matched'
    assert [candidate.name for candidate in match.candidates] == ['ExistingThing']


def test_no_match_when_field_sets_differ(tmp_path: Path) -> None:
    """Verify unrelated field sets produce no candidate.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
            beta: int
        """,
        {
            '__init__.py': """
                from wxc_sdk.base import ApiModel


                class ExistingThing(ApiModel):
                    alpha: str
                    gamma: int
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'no_match'
    assert match.candidates == ()


def test_superset_candidate_reported_when_no_exact_match(tmp_path: Path) -> None:
    """Verify strict SDK field supersets are reported without exact matches.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
            beta: int
        """,
        {
            '__init__.py': """
                from wxc_sdk.base import ApiModel


                class ExistingThing(ApiModel):
                    alpha: str
                    beta: int
                    gamma: bool
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'superset'
    assert match.candidates == ()
    assert [candidate.model.name for candidate in match.superset_candidates] == ['ExistingThing']
    assert match.superset_candidates[0].extra_fields == frozenset({'gamma'})


def test_superset_candidate_requires_common_primitive_types_to_match(tmp_path: Path) -> None:
    """Verify primitive type mismatches reject superset candidates.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
        """,
        {
            '__init__.py': """
                from wxc_sdk.base import ApiModel


                class ExistingThing(ApiModel):
                    alpha: int
                    beta: bool
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'no_match'
    assert match.superset_candidates == ()


def test_superset_candidate_can_come_from_inherited_sdk_fields(tmp_path: Path) -> None:
    """Verify inherited SDK fields participate in superset matching.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from typing import Optional

        from wxc_sdk.base import ApiModel


        class GeneratedWelcomeMessage(ApiModel):
            enabled: Optional[bool] = None
            always_enabled: Optional[bool] = None
            greeting: Optional[GeneratedGreeting] = None
            audio_announcement_files: Optional[list[GeneratedAudioFile]] = None
        """,
        {
            '__init__.py': """
                from typing import Optional

                from wxc_sdk.base import ApiModel


                class AudioSource(ApiModel):
                    enabled: bool
                    greeting: Greeting
                    audio_announcement_files: list[AnnAudioFile]
                    audio_playlist_id: Optional[str] = None


                class WelcomeMessageSetting(AudioSource):
                    always_enabled: bool
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedWelcomeMessage']

    assert match.status == 'superset'
    assert [candidate.model.name for candidate in match.superset_candidates] == ['WelcomeMessageSetting']
    assert match.superset_candidates[0].extra_fields == frozenset({'audio_playlist_id'})


def test_multiple_sdk_candidates_are_reported(tmp_path: Path) -> None:
    """Verify all exact SDK candidates are reported.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
        """,
        {
            'first.py': """
                from wxc_sdk.base import ApiModel


                class FirstThing(ApiModel):
                    alpha: str
            """,
            'second.py': """
                from wxc_sdk.base import ApiModel


                class SecondThing(ApiModel):
                    alpha: str
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'matched'
    assert [candidate.name for candidate in match.candidates] == ['FirstThing', 'SecondThing']


def test_inherited_sdk_fields_are_merged(tmp_path: Path) -> None:
    """Verify inherited SDK fields can create an exact field-set match.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
            beta: int
        """,
        {
            '__init__.py': """
                from wxc_sdk.base import ApiModel


                class BaseThing(ApiModel):
                    alpha: str


                class ChildThing(BaseThing):
                    beta: int
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'matched'
    assert [candidate.name for candidate in match.candidates] == ['ChildThing']


def test_aliases_do_not_make_models_equivalent(tmp_path: Path) -> None:
    """Verify serialized aliases are ignored for generated-mode equivalence.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :return: ``None``.
    :rtype: None
    """
    result = analyze(
        tmp_path,
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            id: str
        """,
        {
            '__init__.py': """
                from pydantic import Field
                from wxc_sdk.base import ApiModel


                class ExistingThing(ApiModel):
                    schedule_id: str = Field(alias='id')
            """,
        },
    )

    match = matches_by_generated_name(result)['GeneratedThing']

    assert match.status == 'no_match'


def test_added_only_excludes_models_present_at_base(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify ``--added-only`` excludes generated classes present at base.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :param monkeypatch: Pytest monkeypatch fixture.
    :type monkeypatch: pytest.MonkeyPatch
    :return: ``None``.
    :rtype: None
    """
    generated_file = write_py(
        tmp_path / 'open_api' / 'generated' / 'feature_auto.py',
        """
        from wxc_sdk.base import ApiModel


        class ExistingGenerated(ApiModel):
            alpha: str


        class NewGenerated(ApiModel):
            beta: str
        """,
    )
    sdk_root = tmp_path / 'wxc_sdk'
    write_py(
        sdk_root / '__init__.py',
        """
        from wxc_sdk.base import ApiModel


        class ExistingSdk(ApiModel):
            alpha: str


        class NewSdk(ApiModel):
            beta: str
        """,
    )

    monkeypatch.setattr(
        fem,
        'load_generated_source_at_ref',
        lambda generated_file, base_ref: textwrap.dedent(
            """
            from wxc_sdk.base import ApiModel


            class ExistingGenerated(ApiModel):
                alpha: str
            """
        ),
    )

    result = fem.analyse_generated_file(generated_file=generated_file, sdk_root=sdk_root, added_only=True)

    assert [match.generated.name for match in result.matches] == ['NewGenerated']
    assert [candidate.name for candidate in result.matches[0].candidates] == ['NewSdk']


def test_added_only_treats_new_generated_file_as_all_added(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify absent base files make all current generated classes new.

    :param tmp_path: Pytest temporary directory.
    :type tmp_path: Path
    :param monkeypatch: Pytest monkeypatch fixture.
    :type monkeypatch: pytest.MonkeyPatch
    :return: ``None``.
    :rtype: None
    """
    generated_file = write_py(
        tmp_path / 'open_api' / 'generated' / 'feature_auto.py',
        """
        from wxc_sdk.base import ApiModel


        class GeneratedThing(ApiModel):
            alpha: str
        """,
    )
    sdk_root = tmp_path / 'wxc_sdk'
    write_py(
        sdk_root / '__init__.py',
        """
        from wxc_sdk.base import ApiModel


        class ExistingThing(ApiModel):
            alpha: str
        """,
    )

    monkeypatch.setattr(fem, 'load_generated_source_at_ref', lambda generated_file, base_ref: None)

    result = fem.analyse_generated_file(generated_file=generated_file, sdk_root=sdk_root, added_only=True)

    assert [match.generated.name for match in result.matches] == ['GeneratedThing']
    assert result.matches[0].status == 'matched'
