# 火星基地资源调度模拟器：V0-V8 章节版本

这些文件用于课堂逐章扩展项目。每个版本都可以独立运行，并且只使用截至对应章节已经讲过的语法。

## 版本地图

| 版本 | 文件 | 本次新增 |
| --- | --- | --- |
| V0 | `v0_first_program.py` | 第一个 Python 文件和 `print()` |
| V1 | `v1_output_comments_debug.py` | 多次输出、注释和基础 Debug 材料 |
| V2 | `v2_variables_types.py` | 变量、标识符、数值、字符串、布尔值和 `type()` |
| V3 | `v3_strings_formatting.py` | f-string、转义字符和状态面板 |
| V4 | `v4_input_operators.py` | `input()`、`int()`、算术与复合赋值 |
| V5 | `v5_boolean_logic.py` | 比较、`and`、`or`、`not` 和布尔表达式 |
| V6 | `v6_conditions.py` | `if-elif-else`、嵌套判断和单日调度 |
| V7 | `v7_while_loops.py` | `while`、输入验证、任务日循环和循环嵌套 |
| V8 | [`../reference-solution/mars_base_simulator.py`](../reference-solution/mars_base_simulator.py) | `for`、`range()`、`break`、`continue` 和最终评级 |

## 使用方式

教师讲解新版本时，应先运行上一版本，再只展示本次新增或修改的代码。不要让学生每章重新输入整个文件。

建议流程：

1. 预测新功能需要增加哪些变量或控制结构。
2. 运行上一版本，确认当前行为。
3. 分段输入新增代码，每段输入后立即运行。
4. 完成对应章节的找错任务。
5. 保存为新的版本文件，再进入下一章。

## 运行示例

在项目根目录执行：

```powershell
py project/chapter-versions/v5_boolean_logic.py
```

macOS 或 Linux 使用：

```bash
python3 project/chapter-versions/v5_boolean_logic.py
```

V0-V7 是教学演进版本，V8 同时也是教师最终参考答案。最终版本不重复保存，以免调度规则和测试基线在两份文件中产生偏差。
