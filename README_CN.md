[<img alt="LOGO" src="http://gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-exception.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-exception/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_exception)](https://pypi.org/project/gqylpy_exception)
[![License](https://img.shields.io/pypi/l/gqylpy_exception)](https://github.com/gqylpy/gqylpy-exception/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/gqylpy_exception)](https://pepy.tech/project/gqylpy_exception)

# gqylpy-exception
[English](README.md) | 中文

`gqylpy-exception` 是一个灵活且便捷的Python异常处理库，允许你动态创建异常类，并提供多种异常处理机制。

<kbd>pip3 install gqylpy_exception</kbd>

## 动态创建异常

使用 `gqylpy-exception`，你可以在需要时即时创建异常类，而无需提前定义。例如，如果你希望抛出一个名为 `NotUnderstandError` 的异常，只需导入库并以如下方式调用：
```python
import gqylpy_exception as ge

raise ge.NotUnderstandError(...)
```

在这里，`NotUnderstandError` 并不是 `gqylpy-exception` 预先定义的，而是在你尝试访问 `ge.NotUnderstandError` 时通过魔化方法 `__getattr__` 动态创建的。这种灵活性意味着你可以根据需要创建任何名称的异常类。

此外，`gqylpy-exception` 还确保不会重复创建相同的异常类。所有已创建的异常类都会被存储在 `ge.__history__` 字典中，以便后续快速访问。

还有一种用法，导入即创建：
```python
from gqylpy_exception import NotUnderstandError

raise NotUnderstandError(...)
```

## 强大的异常处理功能

`gqylpy-exception` 还提供了一系列强大的异常处理工具：
- `TryExcept`: 装饰器，捕获被装饰的函数中引发的异常，并将异常信息输出到终端（不是抛出）。这有助于避免程序因未处理的异常而崩溃。
- `Retry`: 装饰器，同上，并会尝试重新执行，通过参数控制次数和每次重试之间的间隔时间，在达到最大次数后抛出异常。
- `TryContext`: 上下文管理器，使用 `with` 语句，你可以轻松捕获代码块中引发的异常，并将异常信息输出到终端。

**使用 `TryExcept` 处理函数中引发的异常**
```python
from gqylpy_exception import TryExcept

@TryExcept(ValueError)
def func():
    int('a')
```
默认的处理方案是将异常简要信息输出到终端，不会中断程序执行。当然，也可以输出到日志或做其它处理，通过参数控制。

> 根据 Python 编程规范，处理异常时应明确指定异常类型。因此，在使用 `TryExcept` 装饰器时，需要明确传递所处理的异常类型。

**使用 `Retry` 重试函数中引发的异常**
```python
from gqylpy_exception import Retry

@Retry(count=3, cycle=1)
def func():
    int('a')
```
若被装饰的函数中引发了异常，会尝试重新执行被装饰的函数，默认重试 `Exception` 及其所有子类的异常。像上面这样调用 `Retry(count=3, cycle=1)` 表示最大执行3次，每次间隔1秒。

`Retry` 可以配合 `TryExcept` 使用，将先重试异常，若重试无果，则在最后处理异常：
```python
from gqylpy_exception import TryExcept, Retry

@TryExcept(ValueError)
@Retry(count=3, cycle=1)
def func():
    int('a')
```

**使用 `TryContext` 处理上下文中引发的异常**
```python
from gqylpy_exception import TryContext

with TryContext(ValueError):
    int('a')
```

通过 `gqylpy-exception`，你可以更加灵活和高效地处理Python程序中的异常，提升代码的健壮性和可靠性。
