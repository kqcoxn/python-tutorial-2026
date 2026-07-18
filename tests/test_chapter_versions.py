import ast
import os
from pathlib import Path
import subprocess
import sys

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
VERSION_DIR = PROJECT_ROOT / "project" / "chapter-versions"

VERSION_FILES = (
    "v0_first_program.py",
    "v1_output_comments_debug.py",
    "v2_variables_types.py",
    "v3_strings_formatting.py",
    "v4_input_operators.py",
    "v5_boolean_logic.py",
    "v6_conditions.py",
    "v7_while_loops.py",
)


def parse_version(filename: str) -> ast.Module:
    source = (VERSION_DIR / filename).read_text(encoding="utf-8")
    return ast.parse(source)


def has_node(tree: ast.Module, node_type: type[ast.AST]) -> bool:
    return any(isinstance(node, node_type) for node in ast.walk(tree))


def has_call(tree: ast.Module, function_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == function_name:
                return True
    return False


def run_version(filename: str, responses: str = "") -> str:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    completed = subprocess.run(
        [sys.executable, str(VERSION_DIR / filename)],
        input=responses,
        capture_output=True,
        check=True,
        encoding="utf-8",
        env=env,
        timeout=5,
    )
    return completed.stdout


@pytest.mark.parametrize("filename", VERSION_FILES)
def test_chapter_version_uses_no_advanced_syntax(filename: str) -> None:
    tree = parse_version(filename)
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


def test_versions_introduce_syntax_in_course_order() -> None:
    v0 = parse_version("v0_first_program.py")
    v1 = parse_version("v1_output_comments_debug.py")
    v2 = parse_version("v2_variables_types.py")
    v3 = parse_version("v3_strings_formatting.py")
    v4 = parse_version("v4_input_operators.py")
    v5 = parse_version("v5_boolean_logic.py")
    v6 = parse_version("v6_conditions.py")
    v7 = parse_version("v7_while_loops.py")

    assert not has_node(v0, ast.Assign)
    assert not has_node(v1, ast.Assign)

    assert has_node(v2, ast.Assign)
    assert not has_node(v2, ast.JoinedStr)
    assert not has_call(v2, "input")
    for early_tree in (v0, v1, v2):
        assert not any(
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and "\n" in node.value
            for node in ast.walk(early_tree)
        )

    assert has_node(v3, ast.JoinedStr)
    assert not has_call(v3, "input")

    assert has_call(v4, "input")
    assert has_call(v4, "int")
    assert not has_node(v4, ast.If)

    assert has_node(v5, ast.BoolOp)
    assert has_node(v5, ast.Compare)
    assert not has_node(v5, ast.If)

    assert has_node(v6, ast.If)
    assert not has_node(v6, ast.While)
    assert not has_node(v6, ast.For)

    assert has_node(v7, ast.While)
    assert not has_node(v7, ast.For)
    assert not has_node(v7, ast.Break)
    assert not has_node(v7, ast.Continue)


@pytest.mark.parametrize(
    ("filename", "responses", "expected_output"),
    [
        (
            "v0_first_program.py",
            "",
            "火星基地资源调度系统启动",
        ),
        (
            "v1_output_comments_debug.py",
            "",
            "系统自检：资源监测模块正常",
        ),
        (
            "v2_variables_types.py",
            "",
            "基地名称： 星火基地",
        ),
        (
            "v3_strings_formatting.py",
            "",
            "基地：星火基地 | 任务日：1/7",
        ),
        (
            "v4_input_operators.py",
            "星火基地\n20\n",
            "星火基地当前剩余能源：80",
        ),
        (
            "v5_boolean_logic.py",
            "25\n20\n15\n",
            "可以开展科研探索：True",
        ),
        (
            "v6_conditions.py",
            "星火基地\n1\n",
            "能源：100 | 氧气：90 | 饮用水：92",
        ),
        (
            "v7_while_loops.py",
            "星火基地\n3\n3\n3\n2\n1\n1\n1\n",
            "任务评价：卓越科研任务",
        ),
    ],
    ids=["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"],
)
def test_chapter_version_runs(
    filename: str,
    responses: str,
    expected_output: str,
) -> None:
    output = run_version(filename, responses)

    assert expected_output in output
