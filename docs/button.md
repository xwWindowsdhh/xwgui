# button 函数

在窗口中显示可点击的按钮，支持直接传递参数。

## 语法

```python
button(text, x, y, func=None, *args)
```

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | str | 是 | 按钮文字 |
| x | int | 是 | 按钮左上角 x 坐标（像素） |
| y | int | 是 | 按钮左上角 y 坐标（像素） |
| func | function | 否 | 点击按钮时执行的函数 |
| *args | any | 否 | 传递给函数的参数，可多个 |

## 返回值

无

## 示例

### 基础用法（无参数）

```python
from window import window
from button import button

def on_click():
    print("按钮被点击了！")

button("确定", 50, 100, on_click)

window("按钮测试", 400, 300)
```

### 传递一个参数

```python
from window import window
from button import button

def greet(name):
    print(f"你好，{name}！")

button("问候张三", 50, 100, greet, "张三")
button("问候李四", 150, 100, greet, "李四")

window("按钮测试", 400, 300)
```

### 传递多个参数

```python
from window import window
from button import button

def add(a, b):
    print(f"{a} + {b} = {a + b}")

button("3+5", 50, 100, add, 3, 5)
button("10+20", 150, 100, add, 10, 20)

window("按钮测试", 400, 300)
```

### 空壳按钮（无功能）

```python
from window import window
from button import button

button("禁用", 50, 100)

window("按钮测试", 400, 300)
```

### 多个按钮组合

```python
from window import window
from characters import characters
from button import button

def login():
    print("正在登录...")

def register():
    print("正在注册...")

characters("用户名:", 50, 50)
characters("密码:", 50, 80)

button("登录", 100, 150, login)
button("注册", 200, 150, register)

window("登录界面", 400, 300)
```

## 特点

- **简单传参**：直接跟在函数后面，无需 lambda 或 args 元组
- **可选回调**：不设置函数时，按钮仅显示无功能
- **视觉反馈**：鼠标悬浮变手型，点击有按下效果
- **自动重绘**：调整窗口大小后按钮自动重绘

## 注意事项

- **必须先调用 `button()` 添加按钮，再调用 `window()` 创建窗口**
- 参数直接跟在函数后面，不需要括号
- 按钮默认尺寸为 80x25 像素
- 按钮文字会自动居中显示
