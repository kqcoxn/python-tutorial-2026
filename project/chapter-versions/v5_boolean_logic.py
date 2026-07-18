print("火星基地科研任务条件检查")

energy = int(input("请输入当前能源："))
oxygen = int(input("请输入当前氧气："))
water = int(input("请输入当前饮用水："))

can_explore = energy >= 20 and oxygen >= 15 and water >= 10
needs_life_support = oxygen < 30 or water < 25
system_safe = energy > 0 and oxygen > 0 and water > 0
system_at_risk = not system_safe

print(f"\n可以开展科研探索：{can_explore}")
print(f"需要维护生命保障系统：{needs_life_support}")
print(f"基地系统安全：{system_safe}")
print(f"基地系统存在风险：{system_at_risk}")
