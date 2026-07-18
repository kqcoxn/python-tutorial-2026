print("==========================================")
print("       火星基地资源调度模拟器")
print("==========================================")
print("系统自检 1/3：正常")
print("系统自检 2/3：正常")
print("系统自检 3/3：正常")

base_name = input("\n请输入火星基地名称：")
if base_name == "":
    base_name = "星火基地"

mission_day = 1
max_days = 7
energy = 100
oxygen = 100
water = 100
research_points = 0
mission_active = True
completed_days = 0

while mission_day <= max_days and mission_active:
    print("\n" + "-" * 42)
    print(f"任务日：{mission_day}/{max_days}")
    print(f"能源：{energy} | 氧气：{oxygen} | 饮用水：{water}")
    print(f"科研积分：{research_points}")
    print("\n1. 维护供能系统")
    print("2. 维护生命保障系统")
    print("3. 开展科研探索")

    choice = input("请输入任务编号（1/2/3）：")
    while choice != "1" and choice != "2" and choice != "3":
        print("无效选择，请重新输入。")
        choice = input("请输入任务编号（1/2/3）：")

    task_completed = True

    if choice == "1":
        energy += 25
        print("供能系统维护完成。")
    elif choice == "2":
        energy -= 15
        oxygen += 20
        water += 15
        print("生命保障系统维护完成。")
    else:
        can_explore = energy >= 20 and oxygen >= 15 and water >= 10
        if can_explore:
            energy -= 20
            oxygen -= 10
            water -= 8
            research_points += 30
            print("科研探索完成，获得 30 点科研积分。")
        else:
            task_completed = False
            print("资源不足，无法开展科研探索，请重新调度。")

    if task_completed:
        energy -= 5
        oxygen -= 10
        water -= 8

        if energy > 100:
            energy = 100
        if oxygen > 100:
            oxygen = 100
        if water > 100:
            water = 100

        completed_days += 1
        print(f"日终资源：能源 {energy}，氧气 {oxygen}，饮用水 {water}")

        if energy <= 0 or oxygen <= 0 or water <= 0:
            mission_active = False
            print("关键资源耗尽，启动应急撤离！")
        else:
            mission_day += 1

print("\n" + "=" * 42)
print(f"{base_name}最终任务报告")
print(f"已完成任务日：{completed_days}/{max_days}")
print(f"能源：{energy} | 氧气：{oxygen} | 饮用水：{water}")
print(f"科研积分：{research_points}")

if not mission_active:
    print("任务评价：应急撤离")
elif research_points >= 90:
    print("任务评价：卓越科研任务")
elif research_points >= 60:
    print("任务评价：火星任务顺利完成")
else:
    print("任务评价：基地稳定运行，科研目标未完全达成")

print("=" * 42)
