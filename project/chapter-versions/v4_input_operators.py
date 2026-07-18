print("火星基地能源计算器")

base_name = input("请输入火星基地名称：")
energy = 100
energy_cost = int(input("请输入本次任务的能源消耗："))

energy -= energy_cost
oxygen = 100
water = 100
total_resources = energy + oxygen + water
average_resource = total_resources / 3

print(f"\n{base_name}当前剩余能源：{energy}")
print(f"三项资源总量：{total_resources}")
print(f"三项资源平均值：{average_resource}")
