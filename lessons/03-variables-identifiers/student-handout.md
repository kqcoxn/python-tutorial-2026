# 第 3 章学生讲义：变量、标识符与基本类型

> 学习路线：先用普通状态卡理解变量与类型，再集中建立火星项目 V2 的状态模型。

## 1. 本章目标

- 创建、读取和重新赋值变量。
- 解释 `=` 的赋值方向。
- 判断变量名是否合法、是否清晰。
- 使用 `snake_case` 命名。
- 识别 `int`、`float`、`str`、`bool`。
- 使用 `type()` 检查值的类型。
- 完成项目 V2 的状态变量。

## 2. 变量保存值

```python
student_name = "小林"
score = 92

print(student_name)
print(score)
```

填写：变量 `student_name` 当前保存 __________________；变量 `score` 当前保存 __________________。

## 3. 重新赋值

先预测：

```python
score = 80
score = 95
print(score)
```

输出：________

执行模型：

```text
计算等号右边 -> 把结果保存到左边名称 -> 原来的值被替换
```

这里的 `=` 表示赋值，不是数学中的“永远相等”。

## 4. 标识符规则

变量名：

- 以字母或下划线开头。
- 后面可以包含字母、数字和下划线。
- 不能有空格、连字符。
- 不能使用 Python 关键字。
- 区分大小写。

判断并修改：

| 名称 | 合法吗 | 如果不合法，修改为 |
| --- | --- | --- |
| `student_name` | ______ | |
| `score2` | ______ | |
| `2score` | ______ | |
| `student name` | ______ | |
| `student-name` | ______ | |
| `class` | ______ | |

合法不等于清晰。`s = 95` 可以运行，但 `student_score = 95` 更容易理解。本课程变量名统一使用简短英文 `snake_case`，输出内容可以使用中文。

## 5. 四种基本类型

```python
student_name = "小林"
score = 92
accuracy = 0.95
is_online = True
```

| 变量 | 类型预测 | `type()` 结果 |
| --- | --- | --- |
| `student_name` | | |
| `score` | | |
| `accuracy` | | |
| `is_online` | | |

运行：

```python
print(type(student_name))
print(type(score))
print(type(accuracy))
print(type(is_online))
```

| 类型 | 例子 | 含义 |
| --- | --- | --- |
| `str` | `"小林"` | 文本 |
| `int` | `92` | 整数 |
| `float` | `0.95` | 小数 |
| `bool` | `True` | 真或假 |

`True`、`False` 首字母大写，不加引号。

## 6. 相似外观，不同类型

```python
number_value = 7
text_value = "7"
flag_value = True
flag_text = "True"
```

| 变量 | 有没有引号 | 类型 |
| --- | --- | --- |
| `number_value` | | |
| `text_value` | | |
| `flag_value` | | |
| `flag_text` | | |

本章先识别类型，第 5 章再学习类型转换。

## 7. 集中编写项目 V2

前面是普通演示。现在从 V1 另存为 `v2_variables_types.py`，建立火星项目状态：

| 变量 | 初始值 | 含义 |
| --- | ---: | --- |
| `base_name` | `"星火基地"` | 基地名称 |
| `mission_day` | `1` | 当前任务日 |
| `max_days` | `7` | 最大任务天数 |
| `energy` | `100` | 能源 |
| `oxygen` | `100` | 氧气 |
| `water` | `100` | 饮用水 |
| `research_points` | `0` | 科研积分 |
| `mission_active` | `True` | 任务是否进行中 |

代码骨架：

```python
base_name = "星火基地"
mission_day = 1
max_days = 7

# TODO：补齐四个资源或积分变量

mission_active = True

print("基地名称：", base_name)
print("当前任务日：", mission_day)

# TODO：继续输出资源、积分和任务状态
```

最后检查：

```python
print(type(base_name))
print(type(energy))
print(type(mission_active))
```

- [ ] `base_name` 是 `str`。
- [ ] `energy` 是 `int`。
- [ ] `mission_active` 是 `bool`。

这些数值是教学模型状态，不代表真实火星工程数据。

## 8. 练习

### 练习 1：追踪值

```python
level = 1
level = 2
level = 5
print(level)
```

预测：________  运行结果：________

### 练习 2：类型预测

分别写出 `18`、`18.0`、`"18"`、`False` 的类型，再用 `type()` 验证。

### 练习 3：修复变量名

将 `2nd score`、`student-name`、`class` 改为合法、清晰的名称。

### 练习 4：个人状态卡

定义昵称、年级、跑步用时、今天是否完成作业四个变量，覆盖四种类型并输出。

### 挑战

V2 为什么不一定需要 `float`？设计一个适合使用 `float` 的附加项目状态，并解释它的含义，但不修改核心规则。

## 9. 快速排错

| 现象 | 检查 |
| --- | --- |
| `NameError` | 是否先赋值、拼写和大小写是否一致 |
| 数字开头报错 | 改为字母开头，如 `score2` |
| `true` 未定义 | 改为 `True` |
| 类型与预期不同 | 检查引号并运行 `type()` |
| 名称能运行但看不懂 | 改为有意义的 `snake_case` |

## 10. 本章速查表

| 目标 | 写法 |
| --- | --- |
| 保存值 | `score = 95` |
| 读取值 | `print(score)` |
| 替换当前值 | 再次写 `score = 新值` |
| 查看类型 | `print(type(score))` |
| 字符串 | `"文字"` |
| 整数 / 小数 | `7` / `7.0` |
| 布尔值 | `True` / `False` |

## 11. 离堂检查

- [ ] 我能解释赋值方向。
- [ ] 我能预测重新赋值后的当前值。
- [ ] 我能判断变量名是否合法且清晰。
- [ ] 我能识别四种基本类型。
- [ ] 我会用 `type()` 验证。
- [ ] 我的 V2 能输出全部项目状态。

仍有疑问：____________________________________________________

