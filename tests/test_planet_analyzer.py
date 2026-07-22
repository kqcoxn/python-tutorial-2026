from copy import deepcopy

import pytest

from project.reference_solution import planet_analyzer as analyzer


@pytest.fixture
def research():
    return analyzer.create_research()


@pytest.mark.parametrize(
    ("planet_name", "expected"),
    [
        ("Aster-4b", analyzer.PRIORITY),
        ("Nereid-7c", analyzer.NOT_RECOMMENDED),
        ("Morrow-5e", analyzer.MORE_OBSERVATION),
        ("Lumen-2b", analyzer.PRIORITY),
    ],
)
def test_catalog_covers_all_screening_results(research, planet_name, expected):
    planet = next(
        planet for planet in research["planets"] if planet["name"] == planet_name
    )

    result = analyzer.evaluate_planet(planet, research["rules"])

    assert result["conclusion"] == expected


def test_screening_boundaries_are_inclusive(research):
    planet = research["planets"][-1]

    result = analyzer.evaluate_planet(planet, research["rules"])

    assert result["conclusion"] == analyzer.PRIORITY
    assert result["risk_tags"] == set()


def test_hard_risk_takes_priority_over_incomplete_observation(research):
    planet = deepcopy(research["planets"][2])
    planet["radiation_level"] = 6

    result = analyzer.evaluate_planet(planet, research["rules"])

    assert result["conclusion"] == analyzer.NOT_RECOMMENDED
    assert any("辐射" in reason for reason in result["reasons"])
    assert any("观测不完整" in reason for reason in result["reasons"])


def test_analyze_research_updates_reports_and_risk_tags(research):
    reports = analyzer.analyze_research(research)

    assert len(reports) == 4
    assert reports[1]["risk_tags"]
    assert research["planets"][1]["risk_tags"]


def test_rule_preview_does_not_pollute_baseline(research):
    analyzer.analyze_research(research)
    before = deepcopy(research)

    preview = analyzer.preview_rule_changes(research, analyzer.CONSERVATIVE_CHANGES)
    changes = analyzer.compare_reports(research["reports"], preview["reports"])

    assert research == before
    assert preview["rules"] != research["rules"]
    assert any(change["planet"] == "Lumen-2b" for change in changes)


def test_complete_interaction_can_inspect_preview_and_report():
    answers = iter(["1", "p", "q"])
    output = []

    research = analyzer.run_planet_analyzer(lambda prompt: next(answers), output.append)

    assert len(research["reports"]) == 4
    assert any("Aster-4b" in line and "优先候选" in line for line in output)
    assert any("保守规则预演" in line for line in output)
    assert any("限制声明" in line for line in output)
