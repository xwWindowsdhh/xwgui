# window 函数

创建并显示一个窗口。

## 语法

```python
window(title, width, height, x=None, y=None)
```

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | str | 是 | 窗口标题 |
| width | int | 是 | 窗口宽度（像素） |
| height | int | 是 | 窗口高度（像素） |
| x | int | 否 | 窗口左上角 x 坐标，默认居中 |
| y | int | 否 | 窗口左上角 y 坐标，默认居中 |

## 返回值

返回窗口句柄（hwnd）。

## 示例

### 基础用法

```python
from window import window

window("Hello xwgui!", 800, 600)
```

### 指定位置

```python
from window import window

window("我的窗口", 400, 300, x=100, y=50)
```

### 创建多个窗口

```python
from window import window

window("窗口1", 400, 300)
window("窗口2", 400, 300)
```

## 注意事项

- 窗口创建后会自动进入消息循环，保持窗口显示
- 点击关闭按钮可以正常关闭窗口
- 支持最大化、最小化、调整大小等标准窗口操作
