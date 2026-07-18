# 第 3 章教师教案：变量、标识符与基本类型

> 更新日期：2026-07-18  
> 建议用时：80-120 分钟，可按模块拆分  
> 项目版本：从 V1 扩展到 V2

## 1. 章节定位

本章第一次让程序“记住状态”。教学重点是赋值执行过程、命名质量和四种基本类型，不提前讲复杂运算。前半段用姓名、分数、准确率和在线状态建立变量模型，后半段集中建立项目 V2 的状态变量。

## 2. 学习目标与验收证据

| 学习目标 | 验收证据 |
| --- | --- |
| 创建、读取和重新赋值变量 | 能预测同一变量最后输出的值 |
| 解释赋值方向 | 能说出“先算右边，再保存到左边” |
| 判断标识符是否合法 | 能修复数字开头、空格、关键字等名称 |
| 使用有意义的 `snake_case` 名称 | 能把 `a`、`x1` 改为表达含义的名称 |
| 识别 `int`、`float`、`str`、`bool` | 能根据值和 `type()` 判断类型 |
| 完成 V2 状态模型 | 正确输出基地名称、任务日、资源、积分和状态 |

最低标准：学生能独立定义四种类型的变量，正确输出并解释至少三个变量名的含义。

## 3. 开始条件与边界

- 已完成 V1。
- 会使用 `print()`、注释和基础排错流程。
- 知道字符串文字需要引号。

本章不讲 `input()`、f-string、条件判断、容器或对象内存模型。`type()` 只作为观察工具，不展开“类”的概念。

## 4. 核心词汇

| 词汇 | 含义 |
| --- | --- |
| 变量 | 保存一个值、可以通过名称读取的位置 |
| 赋值 | 计算右侧并把结果保存到左侧名称 |
| 标识符 | 变量等程序元素使用的名称 |
| 类型 | 值所属的类别 |
| 重新赋值 | 用新值替换变量当前保存的值 |
| `snake_case` | 小写单词用下划线连接的命名风格 |

## 5. 教学流程

| 模块 | 建议用时 | 产出 |
| --- | ---: | --- |
| A. 变量与赋值 | 15-20 分钟 | 能追踪当前值 |
| B. 标识符与命名 | 15-20 分钟 | 能判断并改善名称 |
| C. 四种基本类型 | 20-25 分钟 | 能用 `type()` 观察 |
| D. V2 集中建模 | 20-35 分钟 | 完成项目状态变量 |
| E. 找错与检查点 | 10-20 分钟 | 独立修复命名和类型问题 |

## 6. 核心教学步骤

### 步骤 1：变量保存值

```python
student_name = "小林"
score = 92

print(student_name)
print(score)
```

用“带标签的盒子”只做一次直观比喻，随后回到执行模型：Python 看到名称时读取它当前保存的值。

### 步骤 2：理解赋值方向和重新赋值

```python
score = 80
score = 95
print(score)
```

运行前预测。预期只输出 `95`，不是同时保存两个分数。

板书：

```text
score = 95
右侧得到 95 -> 将 95 保存到 score -> 原来的 80 被替换
```

强调此处 `=` 不是数学中的恒等关系；相等比较到第 6 章使用 `==`。

### 步骤 3：判断标识符是否合法

合法示例：

```python
student_name = "小林"
score2 = 95
is_online = True
```

需要修复的示例：

```text
2score        数字开头
student name  包含空格
class         Python 关键字
```

规则：字母或下划线开头，后面可含字母、数字、下划线；区分大小写；不能使用关键字。Python 技术上允许部分非英文名称，但本课程统一使用简短的英文 `snake_case`，输出文字仍可使用中文。

命名讨论：`s = 95` 合法但含义弱，`student_score = 95` 更适合长期阅读。

### 步骤 4：认识四种基本类型

```python
student_name = "小林"
score = 92
accuracy = 0.95
is_online = True

print(type(student_name))
print(type(score))
print(type(accuracy))
print(type(is_online))
```

| 类型 | 示例 | 直观含义 |
| --- | --- | --- |
| `str` | `"小林"` | 文本 |
| `int` | `92` | 整数 |
| `float` | `0.95` | 带小数的数值 |
| `bool` | `True` | 真或假 |

强调 `True`、`False` 首字母大写且不加引号；`"92"` 是字符串，不是整数。

### 步骤 5：值相似不等于类型相同

```python
number_value = 7
text_value = "7"
flag_value = True
flag_text = "True"

print(type(number_value))
print(type(text_value))
print(type(flag_value))
print(type(flag_text))
```

让学生先按“有没有引号”预测。此处不进行类型转换，转换留到第 5 章。

### 步骤 6：切换到项目 V2

明确提示：“现在开始用变量建立火星项目状态。”从 V1 另存为 `v2_variables_types.py`，建立：

| 变量 | 初始值 | 类型与含义 |
| --- | --- | --- |
| `base_name` | `"星火基地"` | `str`，基地名称 |
| `mission_day` | `1` | `int`，当前任务日 |
| `max_days` | `7` | `int`，最大天数 |
| `energy` | `100` | `int`，能源 |
| `oxygen` | `100` | `int`，氧气 |
| `water` | `100` | `int`，饮用水 |
| `research_points` | `0` | `int`，科研积分 |
| `mission_active` | `True` | `bool`，任务是否进行中 |

使用多个参数输出，不提前使用 f-string：

```python
print("基地名称：", base_name)
print("当前任务日：", mission_day)
```

最后用 `type()` 检查 `base_name`、`energy`、`mission_active`。所有数值都是教学模型状态。

## 7. 常见误解与排查

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `NameError` | 先使用后赋值或拼写不一致 | 找到首次赋值，逐字符对照名称 |
| `SyntaxError: invalid decimal literal` | 名称以数字开头 | 改为字母开头，如 `score2` |
| `True` 被当作未定义名称 | 写成了 `true` | 使用首字母大写的 `True` |
| 输出带引号的数字被认为是整数 | 忽略引号 | 用 `type()` 验证 |
| `studentName`、`StudentName` 混用 | 大小写不一致 | 统一为 `student_name` |
| 合法但难读 | 使用 `a`、`x1` 等弱名称 | 根据状态含义重新命名 |

## 8. 练习与答案

### 跟随练习 1：追踪当前值

```python
level = 1
level = 2
level = 5
print(level)
```

答案：`5`。

### 跟随练习 2：类型预测

预测 `18`、`18.0`、`"18"`、`False` 的类型，再使用 `type()` 验证。

### 独立练习 1：修复名称

将 `2nd score`、`student-name`、`class` 分别改成合法且清晰的变量名。参考：`second_score`、`student_name`、`course_name`。

### 独立练习 2：个人状态卡

定义昵称、年级、跑步用时和今天是否完成作业四个变量，覆盖四种类型并输出。

### 挑战：最少的类型

判断 V2 为什么没有必须使用 `float`。再提出一个适合增加 `float` 状态的项目指标，但不修改核心版规则。

## 9. 章节检查点

- [ ] 能解释赋值从右向左保存。
- [ ] 能预测重新赋值后的最终值。
- [ ] 能判断常见标识符是否合法。
- [ ] 能识别 `int`、`float`、`str`、`bool`。
- [ ] 能用 `type()` 验证而不是只凭猜测。
- [ ] V2 的八个状态变量名称、值和类型合理。
- [ ] 项目输出中能看到基地名称、资源、积分和任务状态。

## 10. 进度调整与速查

进度快：增加命名互评、相似值不同类型和大小写找错题。进度慢：先保留赋值、合法名称、`int/str/bool` 和 V2 核心变量，`float` 类型讨论可后移。

| 目标 | 写法 |
| --- | --- |
| 赋值 | `score = 95` |
| 重新赋值 | 再写一次 `score = 新值` |
| 观察类型 | `type(score)` |
| 布尔值 | `True`、`False` |
| 推荐命名 | `student_score` |

- 上一版本：`project/chapter-versions/v1_output_comments_debug.py`
- 本章答案：`project/chapter-versions/v2_variables_types.py`
- 下一版本：`project/chapter-versions/v3_strings_formatting.py`

