# 第 1 章学生讲义：运行你的第一个 Python 程序

> 你会先运行传统的 `Hello, Python!`，再把同样的输出知识用于火星基地项目 V0。

## 1. 本章任务

完成后，你应该能够：

- 找到 Python 解释器。
- 在 PyCharm 中创建项目和 `.py` 文件。
- 使用 `print()` 输出文字。
- 修改程序并重新运行。
- 知道代码区、运行按钮和输出区在哪里。

最终检查程序：

```python
print("Hello, Python!")
```

## 2. 四个名称

| 名称 | 它的作用 |
| --- | --- |
| Python | 我们学习的编程语言 |
| Python 解释器 | 读取并执行 Python 代码 |
| `.py` 文件 | 保存 Python 代码的文本文件 |
| PyCharm | 创建、编辑、运行和调试代码的工具 |

运行过程：

```text
.py 文件中的代码 -> Python 解释器 -> 运行结果
                ↑
        PyCharm 帮助我们操作
```

## 3. 安装前检查

先确认自己的操作系统：

- [ ] Windows
- [ ] macOS Apple Silicon
- [ ] macOS Intel
- [ ] 不确定，需要助教确认

只从官方网站下载安装包：

- [Python 官方下载](https://www.python.org/downloads/)
- [PyCharm 官方下载](https://www.jetbrains.com/pycharm/download/)

不要使用来历不明的第三方下载站，也不要通过关闭安全设置解决安装问题。

## 4. Windows 安装与验证

### 4.1 安装 Python

1. 打开 Python 官方下载页。
2. 下载教师指定的稳定 Python 3 Windows 64 位安装包。
3. 启动安装程序。
4. 如果安装界面提供 Add Python to PATH，勾选它。
5. 按教师指定选项完成安装。

打开 PowerShell，执行：

```powershell
py --version
```

预期看到类似结果：

```text
Python 3.x.x
```

如果 `py` 不可用，再尝试：

```powershell
python --version
```

### 4.2 安装 PyCharm

1. 从 JetBrains 官方页面下载 Windows 版本。
2. 安装并启动 PyCharm。
3. 使用免费可用功能，不需要购买专业功能。
4. 创建普通 Python 项目。
5. 确认项目解释器显示 Python 3.x。

## 5. macOS 安装与验证

### 5.1 确认芯片类型

打开“关于本机”：

- 显示 Apple M 系列：选择 Apple Silicon 版本。
- 显示 Intel：选择 Intel 版本。

### 5.2 安装 Python

1. 从 Python 官方页面下载教师指定的 macOS 安装包。
2. 打开 `.pkg` 文件并完成安装。
3. 不使用系统自带的旧 Python 作为课程解释器。

打开终端，执行：

```bash
python3 --version
```

预期看到：

```text
Python 3.x.x
```

### 5.3 安装 PyCharm

1. 下载与芯片匹配的 PyCharm 版本。
2. 将 PyCharm 放入“应用程序”。
3. 启动并创建普通 Python 项目。
4. 项目解释器选择刚安装的 Python 3.x。

## 6. 创建第一个项目

1. 打开 PyCharm。
2. 选择 New Project。
3. 项目位置使用容易找到的目录，例如 `python-course`。
4. 确认解释器是 Python 3.x。
5. 创建项目。
6. 新建 Python 文件 `main.py`。

在窗口中找到：

- [ ] 项目文件区
- [ ] 代码编辑区
- [ ] 运行按钮
- [ ] 运行结果区

## 7. 运行传统的第一个程序

切换到英文输入法，输入：

```python
print("Hello, Python!")
```

运行后检查：

- [ ] 没有红色错误信息。
- [ ] 输出区出现 `Hello, Python!`。
- [ ] 我知道刚才运行的是 `main.py`。

## 8. 理解 `print()`

```python
print("需要显示的文字")
```

- `print`：告诉 Python 显示内容。
- `()`：括号中的内容交给 `print`。
- `""`：引号之间是字符串，也就是一段文字。

注意：代码中的引号和括号使用英文半角符号，并且必须成对出现。

## 9. 预测、修改与玩梗

### 任务 A：增加第二行

在 `main.py` 中加入：

```python
print("人生苦短，我用 Python。")
```

也可以改成自己的短句，例如：

```python
print("我写的不是 Bug，是隐藏功能。")
```

### 任务 B：预测顺序

交换两行 `print()` 前，先写下新的输出顺序，再运行验证。

### 任务 C：字母玩梗

运行前先写出下面程序的输出顺序：

```python
print("B")
print("A")
print("S")
print("E")
```

我的预测：____________________________

## 10. 集中编写火星项目 V0

前面是最小语法演示。现在新建项目文件 `v0_first_program.py`，把已经掌握的 `print()` 集中用于贯穿项目。

逐行输入：

```python
print("==================================")
print("火星基地资源调度系统启动")
print("任务目标：让基地稳定运行 7 天")
print("==================================")
```

运行后检查：

- [ ] 没有红色错误信息。
- [ ] 输出顺序与代码顺序相同。
- [ ] 输出中出现“火星基地资源调度系统启动”。

### 项目练习 A：自定义基地

将“火星基地资源调度系统”改成自己设计的基地名称。

### 项目练习 B：增加任务信息

新增一行输出：

```text
首要目标：保持资源稳定
```

### 项目练习 C：独立检查任务

新建 `mission_card.py`，独立输出：

```text
基地名称：自己设计
任务周期：7 天
首要目标：保持资源稳定
```

要求：

- 文件名是 `mission_card.py`。
- 至少使用三次 `print()`。
- 不修改原来的 `main.py`。
- 能够独立运行。

## 11. 快速排错

| 现象 | 先检查什么 |
| --- | --- |
| 运行按钮不可用 | 项目是否选择了 Python 3.x 解释器 |
| 找不到输出 | 窗口底部的运行结果区是否打开 |
| 修改后输出不变 | 当前运行的是否是另一个文件 |
| 引号附近出现 `SyntaxError` | 是否使用英文引号，左右引号是否齐全 |
| 括号附近出现 `SyntaxError` | 左右括号是否成对 |
| Windows 找不到 Python | 尝试 `py --version` |
| macOS 找不到 Python | 使用 `python3 --version` |

遇到问题时：

1. 不要连续随意修改多处。
2. 找到红色信息指向的行。
3. 检查该行的引号和括号。
4. 说明你认为的一个原因，再请助教协助。

## 12. 备用运行方式

### 本地有 Python，但 PyCharm 暂时不可用

使用随 Python 安装的 IDLE，新建文件后运行。

### 本地环境不可用，但能够联网

打开 [Online Python](https://www.online-python.com/)，在编辑区输入代码并点击 Run。

在线环境是临时方案，课后仍需完成本地环境配置。

## 13. 本章速查表

| 操作 | Windows | macOS |
| --- | --- | --- |
| 检查 Python | `py --version` | `python3 --version` |
| Python 文件扩展名 | `.py` | `.py` |
| 输出文字 | `print("文字")` | `print("文字")` |
| 临时在线环境 | [Online Python](https://www.online-python.com/) | [Online Python](https://www.online-python.com/) |

## 14. 离堂检查

- [ ] 我能说出 PyCharm 和 Python 解释器的区别。
- [ ] 我能创建新的 `.py` 文件。
- [ ] 我能独立运行三行 `print()`。
- [ ] 我知道在哪里查看运行结果。
- [ ] 修改代码后，我会重新运行并检查输出。

仍未完成的步骤：____________________________
