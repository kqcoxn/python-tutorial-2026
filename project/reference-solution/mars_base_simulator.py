print("=" * 42)
print("       火星基地资源调度模拟器")
print("=" * 42)
print("任务目标：让基地稳定运行 7 天，并尽可能获得科研积分。")
print("说明：所有资源数值均为编程教学使用的模拟数值。")

for check_number in range(1, 4):
    print(f"系统自检 {check_number}/3：正常")

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

print(f"\n{base_name}任务控制台已启动。")

while mission_day <= max_days and mission_active:
    print("\n" + "-" * 42)
    print(f"任务日：{mission_day}/{max_days}")
    print(f"能源：{energy} | 氧气：{oxygen} | 饮用水：{water}")
    print(f"科研积分：{research_points}")
    print("\n请选择今日调度任务：")
    print("1. 维护供能系统      能源 +25")
    print("2. 维护生命保障系统  能源 -15，氧气 +20，饮用水 +15")
    print("3. 开展科研探索      能源 -20，氧气 -10，饮用水 -8，科研积分 +30")

    choice = input("请输入任务编号（1/2/3）：")

    if choice == "1":
        energy += 25
        print("供能系统维护完成。")
    elif choice == "2":
        energy -= 15
        oxygen += 20
        water += 15
        print("生命保障系统维护完成。")
    elif choice == "3":
        can_explore = energy >= 20 and oxygen >= 15 and water >= 10
        if not can_explore:
            print("当前资源不足，无法开展科研探索，请重新调度。")
            continue
        energy -= 20
        oxygen -= 10
        water -= 8
        research_points += 30
        print("科研探索完成，获得 30 点科研积分。")
    else:
        print("无效选择，请输入 1、2 或 3。")
        continue

    # 每个有效任务日都要维持基地的基础运行。
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

    print("\n任务日结束后的资源状态：")
    print(f"能源：{energy} | 氧气：{oxygen} | 饮用水：{water}")
    print(f"科研积分：{research_points}")

    if energy <= 0 or oxygen <= 0 or water <= 0:
        mission_active = False
        depleted_resource = "饮用水"
        if energy <= 0:
            depleted_resource = "能源"
        elif oxygen <= 0:
            depleted_resource = "氧气"
        print(
            f"第 {mission_day} 个任务日{depleted_resource}耗尽，"
            "启动应急撤离！"
        )
        break

    mission_day += 1

print("\n" + "=" * 42)
print(f"{base_name}最终任务报告")
print("=" * 42)
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
