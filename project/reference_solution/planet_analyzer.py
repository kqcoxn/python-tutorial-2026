"""“群星彼岸·候选行星分析器”教师参考实现。

程序使用教学化筛查规则，不代表真实的行星宜居性科学结论。
"""

from copy import deepcopy


PRIORITY = "优先候选"
MORE_OBSERVATION = "需要更多观测"
NOT_RECOMMENDED = "不建议继续"

BASELINE_RULES = {
    "temperature_range": (-20.0, 40.0),
    "gravity_range": (0.65, 1.30),
    "pressure_range": (0.50, 1.50),
    "max_radiation": 5,
}

CONSERVATIVE_CHANGES = {
    "temperature_range": (-15.0, 35.0),
    "gravity_range": (0.70, 1.20),
    "pressure_range": (0.60, 1.40),
    "max_radiation": 4,
}


def create_planets():
    """创建覆盖正常、风险、不完整和边界场景的候选目录。"""
    return [
        {
            "name": "Aster-4b",
            "temperature_c": 18.0,
            "gravity_g": 0.92,
            "pressure_atm": 1.10,
            "water_signal": True,
            "radiation_level": 2,
            "observation_complete": True,
            "observation_note": "基础光谱和辐射观测已完成",
            "risk_tags": set(),
        },
        {
            "name": "Nereid-7c",
            "temperature_c": 12.0,
            "gravity_g": 1.42,
            "pressure_atm": 0.90,
            "water_signal": True,
            "radiation_level": 3,
            "observation_complete": True,
            "observation_note": "水信号明确，但重力读数偏高",
            "risk_tags": set(),
        },
        {
            "name": "Morrow-5e",
            "temperature_c": 7.0,
            "gravity_g": 0.81,
            "pressure_atm": 0.72,
            "water_signal": True,
            "radiation_level": 4,
            "observation_complete": False,
            "observation_note": "云层遮挡，需要补充大气成分观测",
            "risk_tags": set(),
        },
        {
            "name": "Lumen-2b",
            "temperature_c": -20.0,
            "gravity_g": 0.65,
            "pressure_atm": 1.50,
            "water_signal": True,
            "radiation_level": 5,
            "observation_complete": True,
            "observation_note": "多项读数位于本次任务的接受边界",
            "risk_tags": set(),
        },
    ]


def create_research():
    """创建一份可独立分析的基准研究状态。"""
    return {
        "rules": BASELINE_RULES.copy(),
        "planets": create_planets(),
        "reports": [],
    }


def evaluate_planet(planet, rules):
    """按教学化规则返回结论、理由和唯一风险标签。"""
    hard_risks = []
    uncertainties = []

    minimum, maximum = rules["temperature_range"]
    temperature = planet["temperature_c"]
    if temperature < minimum or temperature > maximum:
        hard_risks.append(
            f"温度 {temperature:.1f} °C 超出 {minimum:.1f} 至 {maximum:.1f} °C"
        )

    minimum, maximum = rules["gravity_range"]
    gravity = planet["gravity_g"]
    if gravity < minimum or gravity > maximum:
        hard_risks.append(
            f"重力 {gravity:.2f} g 超出 {minimum:.2f} 至 {maximum:.2f} g"
        )

    minimum, maximum = rules["pressure_range"]
    pressure = planet["pressure_atm"]
    if pressure < minimum or pressure > maximum:
        hard_risks.append(
            f"大气压力 {pressure:.2f} atm 超出 {minimum:.2f} 至 {maximum:.2f} atm"
        )

    radiation = planet["radiation_level"]
    if radiation > rules["max_radiation"]:
        hard_risks.append(
            f"辐射等级 {radiation} 高于上限 {rules['max_radiation']}"
        )

    if not planet["water_signal"]:
        uncertainties.append("尚未探测到明确的液态水信号")
    if not planet["observation_complete"]:
        uncertainties.append(f"关键观测不完整：{planet['observation_note']}")

    if hard_risks:
        conclusion = NOT_RECOMMENDED
        reasons = hard_risks + uncertainties
    elif uncertainties:
        conclusion = MORE_OBSERVATION
        reasons = uncertainties
    else:
        conclusion = PRIORITY
        reasons = [
            "温度、重力、大气压力和辐射均通过本次任务筛查",
            "存在液态水信号，且当前要求的观测已经完成",
        ]

    return {
        "conclusion": conclusion,
        "reasons": reasons,
        "risk_tags": set(hard_risks + uncertainties),
    }


def analyze_research(research):
    """分析全部候选并更新当前研究状态。"""
    research["reports"].clear()
    for planet in research["planets"]:
        evaluation = evaluate_planet(planet, research["rules"])
        planet["risk_tags"] = evaluation["risk_tags"].copy()
        research["reports"].append(
            {
                "planet": planet["name"],
                "conclusion": evaluation["conclusion"],
                "reasons": evaluation["reasons"].copy(),
                "risk_tags": evaluation["risk_tags"].copy(),
            }
        )
    return research["reports"]


def preview_rule_changes(research, rule_changes):
    """在深拷贝中应用新规则，避免污染基准研究。"""
    preview = deepcopy(research)
    preview["rules"].update(rule_changes)
    analyze_research(preview)
    return preview


def find_report(reports, planet_name):
    """按候选名称查找报告。"""
    for report in reports:
        if report["planet"] == planet_name:
            return report
    return None


def compare_reports(baseline_reports, preview_reports):
    """找出两套规则下结论发生变化的候选。"""
    changes = []
    for baseline in baseline_reports:
        preview = find_report(preview_reports, baseline["planet"])
        if preview is not None and preview["conclusion"] != baseline["conclusion"]:
            changes.append(
                {
                    "planet": baseline["planet"],
                    "before": baseline["conclusion"],
                    "after": preview["conclusion"],
                }
            )
    return changes


def build_research_report(research):
    """生成基准规则下的最终研究报告。"""
    lines = ["\n=== 群星彼岸 · 候选行星研究报告 ==="]
    priority_names = []

    for report in research["reports"]:
        lines.append(f"- {report['planet']}：{report['conclusion']}")
        for reason in report["reasons"]:
            lines.append(f"    · {reason}")
        if report["conclusion"] == PRIORITY:
            priority_names.append(report["planet"])

    if priority_names:
        lines.append(f"优先候选：{', '.join(priority_names)}")
    else:
        lines.append("当前不推荐任何候选，建议补充观测或复核规则。")
    lines.append(
        "限制声明：以上结果只依据本次教学化筛查规则，不能替代真实科研评估。"
    )
    return lines


def display_catalog(research, output_fn):
    """显示候选名称和基准结论。"""
    output_fn("\n候选目录：")
    for number, report in enumerate(research["reports"], start=1):
        output_fn(f"  {number}. {report['planet']}：{report['conclusion']}")


def display_report_details(report, output_fn):
    """显示一颗候选的完整证据。"""
    output_fn(f"\n[{report['planet']}] {report['conclusion']}")
    for reason in report["reasons"]:
        output_fn(f"  - {reason}")


def display_rule_preview(research, output_fn):
    """显示保守规则预演及结论变化。"""
    preview = preview_rule_changes(research, CONSERVATIVE_CHANGES)
    changes = compare_reports(research["reports"], preview["reports"])
    output_fn("\n=== 保守规则预演（基准研究不会改变） ===")
    if not changes:
        output_fn("本次规则修改没有改变候选结论。")
    for change in changes:
        output_fn(
            f"{change['planet']}：{change['before']} -> {change['after']}"
        )


def run_planet_analyzer(input_fn, output_fn):
    """运行完整候选分析器，并返回基准研究状态。"""
    research = create_research()
    analyze_research(research)
    output_fn("群星彼岸·候选行星分析器")
    output_fn("所有结论均来自本次教学化筛查规则。")

    while True:
        display_catalog(research, output_fn)
        choice = input_fn("输入候选编号查看证据，P 比较规则，或 Q 生成报告：").strip().lower()
        if choice == "q":
            break
        if choice == "p":
            display_rule_preview(research, output_fn)
            continue

        choices = {}
        for number, report in enumerate(research["reports"], start=1):
            choices[str(number)] = report
        if choice not in choices:
            output_fn("无效指令，请输入候选编号、P 或 Q。")
            continue
        display_report_details(choices[choice], output_fn)

    for line in build_research_report(research):
        output_fn(line)
    return research


def main():
    """程序入口。"""
    run_planet_analyzer(input, print)


if __name__ == "__main__":
    main()
