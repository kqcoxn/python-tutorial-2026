import ast
import os
from pathlib import Path
import subprocess
import sys

import pytest


SCRIPT_PATH = (
    Path(__file__).parents[1]
    / "project"
    / "reference-solution"
    / "mars_base_simulator.py"
)


def run_simulation(*responses: str) -> str:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        input="\n".join(responses) + "\n",
        capture_output=True,
        check=True,
        encoding="utf-8",
        env=env,
        timeout=5,
    )
    return completed.stdout


@pytest.mark.parametrize(
    ("choices", "expected_rating", "expected_research"),
    [
        (
            ("1", "1", "1", "1", "1", "1", "1"),
            "任务评价：基地稳定运行，科研目标未完全达成",
            "科研积分：0",
        ),
        (
            ("3", "3", "1", "1", "1", "1", "1"),
            "任务评价：火星任务顺利完成",
            "科研积分：60",
        ),
        (
            ("3", "3", "3", "2", "1", "1", "1"),
            "任务评价：卓越科研任务",
            "科研积分：90",
        ),
    ],
    ids=["stable-only", "mission-complete", "outstanding"],
)
def test_completed_mission_ratings(
    choices: tuple[str, ...],
    expected_rating: str,
    expected_research: str,
) -> None:
    output = run_simulation("星火基地", *choices)

    assert expected_rating in output
    assert expected_research in output
    assert "已完成任务日：7/7" in output


def test_four_research_days_trigger_emergency_evacuation() -> None:
    output = run_simulation("星火基地", "3", "3", "3", "3")

    assert "第 4 个任务日能源耗尽" in output
    assert "任务评价：应急撤离" in output
    assert "已完成任务日：4/7" in output


def test_outstanding_strategy_requires_life_support_maintenance() -> None:
    output = run_simulation(
        "星火基地",
        "3",
        "3",
        "3",
        "1",
        "1",
        "1",
        "1",
    )

    assert "第 7 个任务日氧气耗尽" in output
    assert "任务评价：应急撤离" in output


def test_research_applies_task_and_daily_resource_costs() -> None:
    output = run_simulation(
        "星火基地",
        "3",
        "3",
        "3",
        "2",
        "1",
        "1",
        "1",
    )

    assert "能源：75 | 氧气：80 | 饮用水：84" in output


def test_invalid_choice_does_not_consume_a_mission_day() -> None:
    output = run_simulation(
        "星火基地",
        "9",
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
    )

    assert "无效选择，请输入 1、2 或 3。" in output
    assert output.count("任务日：1/7") == 2
    assert "已完成任务日：7/7" in output


def test_empty_base_name_uses_default_name() -> None:
    output = run_simulation("", "1", "1", "1", "1", "1", "1", "1")

    assert "星火基地任务控制台" in output


def test_student_solution_stays_within_taught_syntax() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_nodes = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Import,
        ast.ImportFrom,
        ast.List,
        ast.ListComp,
        ast.Dict,
        ast.DictComp,
        ast.Set,
        ast.SetComp,
        ast.Tuple,
        ast.Try,
        ast.With,
    )

    assert not any(isinstance(node, forbidden_nodes) for node in ast.walk(tree))
    assert any(isinstance(node, ast.While) for node in ast.walk(tree))
    assert any(isinstance(node, ast.For) for node in ast.walk(tree))
    assert any(isinstance(node, ast.Break) for node in ast.walk(tree))
    assert any(isinstance(node, ast.Continue) for node in ast.walk(tree))
