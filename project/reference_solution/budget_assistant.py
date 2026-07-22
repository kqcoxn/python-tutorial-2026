"""“我的一周预算助手”教师参考实现。"""


NORMAL = "预算正常"
WARNING = "接近预算上限"
EXACT = "预算恰好用完"
OVER_BUDGET = "已经超支"


def read_positive_integer(prompt, input_fn, output_fn):
    """持续读取正整数，不让无效文本进入预算计算。"""
    while True:
        text = input_fn(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        output_fn("请输入大于 0 的整数金额。")


def calculate_budget_status(weekly_budget, total_spent):
    """根据总支出返回预算状态、余额、比例和建议。"""
    remaining = weekly_budget - total_spent
    spending_ratio = total_spent / weekly_budget

    if total_spent > weekly_budget:
        status = OVER_BUDGET
        advice = f"已经超出 {abs(remaining)} 元，建议暂停非必要支出。"
    elif total_spent == weekly_budget:
        status = EXACT
        advice = "本周预算已经全部使用，新增支出将导致超支。"
    elif spending_ratio >= 0.80:
        status = WARNING
        advice = "请复核本周剩余的必要支出。"
    else:
        status = NORMAL
        advice = "预算仍有余量，继续记录才能保持判断准确。"

    return {
        "status": status,
        "remaining": remaining,
        "spending_ratio": spending_ratio,
        "advice": advice,
    }


def display_budget_snapshot(weekly_budget, total_spent, output_fn):
    """显示记录一笔支出后的即时状态。"""
    result = calculate_budget_status(weekly_budget, total_spent)
    output_fn(
        f"累计支出：{total_spent} 元 | 剩余预算：{result['remaining']} 元 | "
        f"已使用：{result['spending_ratio']:.0%}"
    )
    output_fn(f"状态：{result['status']}。{result['advice']}")


def build_budget_report(
    weekly_budget,
    total_spent,
    expense_count,
    food_total,
    transport_total,
    study_total,
    other_total,
):
    """生成最终汇总需要逐行显示的文本。"""
    result = calculate_budget_status(weekly_budget, total_spent)
    if expense_count == 0:
        average_expense = 0
    else:
        average_expense = total_spent / expense_count

    return [
        "\n=== 我的一周预算报告 ===",
        f"一周预算：{weekly_budget} 元",
        f"总支出：{total_spent} 元",
        f"记录笔数：{expense_count}",
        f"平均每笔：{average_expense:.2f} 元",
        f"餐饮：{food_total} 元",
        f"交通：{transport_total} 元",
        f"学习：{study_total} 元",
        f"其他：{other_total} 元",
        f"最终状态：{result['status']}",
        f"建议：{result['advice']}",
        "说明：预算提醒只依据你设定的目标，不代表统一的消费标准。",
    ]


def run_budget_assistant(input_fn, output_fn):
    """运行完整预算助手，并返回最终状态以便复核。"""
    output_fn("我的一周预算助手")
    output_fn("输入整数金额；输入 Q 可以结束记录并查看报告。")
    weekly_budget = read_positive_integer("请输入本周预算：", input_fn, output_fn)

    total_spent = 0
    expense_count = 0
    food_total = 0
    transport_total = 0
    study_total = 0
    other_total = 0

    while True:
        amount_text = input_fn("请输入支出金额，或输入 Q 结束：").strip().lower()
        if amount_text == "q":
            break
        if not amount_text.isdigit() or int(amount_text) <= 0:
            output_fn("支出金额必须是大于 0 的整数。")
            continue

        output_fn("类别：F 餐饮 / T 交通 / S 学习 / O 其他")
        category = input_fn("请选择类别：").strip().lower()
        amount = int(amount_text)

        if category == "f":
            food_total += amount
        elif category == "t":
            transport_total += amount
        elif category == "s":
            study_total += amount
        elif category == "o":
            other_total += amount
        else:
            output_fn("类别无效，这笔支出没有被记录。")
            continue

        total_spent += amount
        expense_count += 1
        display_budget_snapshot(weekly_budget, total_spent, output_fn)

    report = build_budget_report(
        weekly_budget,
        total_spent,
        expense_count,
        food_total,
        transport_total,
        study_total,
        other_total,
    )
    for line in report:
        output_fn(line)

    return {
        "weekly_budget": weekly_budget,
        "total_spent": total_spent,
        "expense_count": expense_count,
        "food_total": food_total,
        "transport_total": transport_total,
        "study_total": study_total,
        "other_total": other_total,
        "status": calculate_budget_status(weekly_budget, total_spent)["status"],
    }


def main():
    """程序入口。"""
    run_budget_assistant(input, print)


if __name__ == "__main__":
    main()
