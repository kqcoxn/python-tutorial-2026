print("==================================")
print("火星基地单日资源调度")
print("==================================")

base_name = input("请输入火星基地名称：")
if base_name == "":
    base_name = "星火基地"

energy = 100
oxygen = 100
water = 100
research_points = 0
task_completed = True

print("\n请选择今日调度任务：")
print("1. 维护供能系统")
print("2. 维护生命保障系统")
print("3. 开展科研探索")
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
    if can_explore:
        energy -= 20
        oxygen -= 10
        water -= 8
        research_points += 30
        print("科研探索完成。")
    else:
        task_completed = False
        print("资源不足，无法开展科研探索。")
else:
    task_completed = False
    print("无效选择。")

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

print(f"\n{base_name}任务结果")
print(f"能源：{energy} | 氧气：{oxygen} | 饮用水：{water}")
print(f"科研积分：{research_points}")
