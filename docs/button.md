# button 函数

在窗口中显示按钮。

## 语法

```python
button(text, x, y, bg_color=0x00C0C0C0, text_color=0x00000000)
```

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | str | 是 | 按钮文字 |
| x | int | 是 | 按钮左上角 x 坐标（像素） |
| y | int | 是 | 按钮左上角 y 坐标（像素） |
| bg_color | int | 否 | 按钮背景颜色，默认浅灰色（0x00C0C0C0） |
| text_color | int | 否 | 按钮文字颜色，默认黑色（0x00000000） |

## 返回值

无

## 示例

### 基础用法

```python
from window import window
from button import button

button("确定", 50, 100)

window("按钮测试", 400, 300)
```

### 多个按钮

```python
from window import window
from button import button

button("确定", 50, 100)
button("取消", 150, 100)
button("帮助", 250, 100)

window("按钮测试", 400, 300)
```

### 文字和按钮一起使用

```python
from window import window
from characters import characters
from button import button

characters("用户名:", 50, 50)
characters("密码:", 50, 80)

button("登录", 100, 150)
button("注册", 200, 150)

window("登录界面", 400, 300)
```

## 注意事项

- **必须先调用 `button()` 添加按钮，再调用 `window()` 创建窗口**
- 按钮默认尺寸为 80x25 像素
- 按钮文字会自动居中显示
- 调整窗口大小后按钮会自动重绘
