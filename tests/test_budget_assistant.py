import pytest

from project.reference_solution import budget_assistant as budget


@pytest.mark.parametrize(
    ("spent", "expected"),
    [
        (200, budget.NORMAL),
        (800, budget.WARNING),
        (1000, budget.EXACT),
        (1001, budget.OVER_BUDGET),
    ],
)
def test_budget_status_covers_normal_warning_exact_and_over(spent, expected):
    result = budget.calculate_budget_status(1000, spent)

    assert result["status"] == expected


def test_complete_budget_session_rejects_invalid_entries():
    answers = iter(
        [
            "0",
            "500",
            "abc",
            "120",
            "x",
            "120",
            "f",
            "80",
            "t",
            "q",
        ]
    )
    output = []

    state = budget.run_budget_assistant(lambda prompt: next(answers), output.append)

    assert state["total_spent"] == 200
    assert state["expense_count"] == 2
    assert state["food_total"] == 120
    assert state["transport_total"] == 80
    assert any("类别无效" in line for line in output)
    assert any("大于 0" in line for line in output)


def test_empty_session_has_zero_average_and_normal_status():
    answers = iter(["500", "q"])
    output = []

    state = budget.run_budget_assistant(lambda prompt: next(answers), output.append)

    assert state["expense_count"] == 0
    assert state["status"] == budget.NORMAL
    assert any("平均每笔：0.00 元" in line for line in output)
