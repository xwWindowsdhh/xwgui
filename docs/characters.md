# characters 函数

在窗口中显示文字。

## 语法

```python
characters(text, x, y, color=0x00000000)
```

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | str | 是 | 要显示的文字内容 |
| x | int | 是 | 文字左上角的 x 坐标（像素） |
| y | int | 是 | 文字左上角的 y 坐标（像素） |
| color | int | 否 | 文字颜色，默认黑色（0x00000000） |

## 返回值

无

## 示例

### 基础用法

```python
from window import window
from characters import characters

characters("Hello xwgui!", 50, 50)

window("文字测试", 800, 600)
```

### 显示多行文字

```python
from window import window
from characters import characters

characters("第一行", 50, 50)
characters("第二行", 50, 80)
characters("第三行", 50, 110)

window("文字测试", 800, 600)
```

### 指定颜色

```python
from window import window
from characters import characters

characters("红色文字", 50, 50, color=0x000000FF)

characters("蓝色文字", 50, 100, color=0x00FF0000)

window("颜色测试", 800, 600)
```

## 注意事项

- **必须先调用 `characters()` 添加文字，再调用 `window()` 创建窗口**
- `window()` 会阻塞直到窗口关闭，所以要在它之前调用 `characters()`
- 坐标原点在窗口左上角，x 向右增加，y 向下增加
- 调整窗口大小后文字会自动重绘
- 颜色格式为 0x00BBGGRR（蓝绿红）
