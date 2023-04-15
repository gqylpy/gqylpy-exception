[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-exception.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-exception/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_exception)](https://pypi.org/project/gqylpy_exception)
[![License](https://img.shields.io/pypi/l/gqylpy_exception)](https://github.com/gqylpy/gqylpy-exception/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_exception/month)](https://pepy.tech/project/gqylpy_exception)

# gqylpy-exception


> 在执行 `raise` 语句的同时创建异常类，无需事先定义异常类，方便快捷。例如，你想抛出一个名为 `NotUnderstandError` 的异常，
> 导入 `import gqylpy_exception as ge` 后直接执行 `raise ge.NotUnderstandError` 即可。
> 
> `gqylpy-exception` 还提供了两个处理异常的装饰器：
> - `TryExcept`: 截获被装饰的函数中引发的异常，并将异常信息输出到终端，不是抛出。
> - `Retry`: 同上，并会尝试重新执行，通过参数控制次数，在达到最大次数后抛出异常。

<kbd>pip3 install gqylpy_exception</kbd>


### 使用 `gqylpy_exception` 创建异常类
```python
import gqylpy_exception as ge

raise ge.AnError(...)
```
`gqylpy_exception` 可以创建任意名称的异常类。`AnError` 不是 `gqylpy_exception` 中内置的，它是在你的代码执行到 `ge.` 
时创建的，魔化方法 `__getattr__` 的特性。你还可以通过魔法方法 `__getitem__` 获得它：
```python
e: ge.GqylpyError = ge['AnError'](...)
```
是的，使用 `gqylpy_exception` 创建的异常类都继承 `GqylpyError`，`GqylpyError` 继承内置的 `Exception`。

还有一种用法，导入即创建：
```python
from gqylpy_exception import AnError

raise AnError(...)
```
另外，`gqylpy_exception` 不会重复创建异常类，创建过的异常类将存入 `ge.__history__` 字典，当你再次创建时从这个字典中取值。


### 使用装饰器 `TryExcept` 处理函数中引发的异常
```python
from gqylpy_exception import TryExcept

@TryExcept(ValueError)
def func():
    int('a')
```
默认的处理流程是将异常简要信息输出到终端。当然，也可以输出到文件或做其它处理，通过参数控制：
```python
def TryExcept(
        etype:      Union[ExceptionTypes],
        *,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ereturn:    Optional[Any]               = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
):
    ...
```
__参数 `etype`__<br>
要处理哪种异常，使用元祖传入多个。

__参数 `silent_exc`__<br>
设为 `True` 将静默处理异常，没有任何输出。

__参数 `raw_exc`__<br>
设为 `True` 将输出完整的异常信息，注意其优先级低于 `silent_exc`。 

__参数 `logger`__<br>
接收一个日志记录器对象，`TryExcept` 希望使用日志记录器输出异常信息，它调用日志记录器的 `error` 方法。<br>
缺省情况下使用 `sys.stderr` 输出异常信息。

__参数 `ereturn`__<br>
若被装饰的函数中引发了异常，将返回此参数，默认为 `None`。<br>
它在某些可以设定非 `None` 默认返回值的函数中非常好用。

__参数 `ecallback`__<br>
接收一个可调用对象，若被装饰的函数中引发了异常将调用它。<br>
这个可调用对象还需接收多个参数：引发的异常对象，被装饰的函数对象，被装饰的函数的所有参数。

__参数 `eexit`__<br>
设为 `True` 将在引发异常后抛出 `SystemExit(4)`，如果有 `ecallback` 则会先执行 `ecallback`。


### 使用装饰器 `Retry` 重试函数中引发的异常
```python
from gqylpy_exception import Retry

@Retry(count=3, cycle=1)
def func():
    int('a')
```
若被装饰的函数中引发了异常，会尝试重新执行被装饰的函数，默认重试 `Exception` 及其子类的所有异常。
像上面这样调用 `Retry(count=3, cycle=1)` 表示最大执行3次，每次间隔1秒。完整的参数如下：
```python
def Retry(
        etype:      Optional[ExceptionTypes]    = None,
        *,
        count:      Optional[int]               = inf,
        cycle:      Optional[Union[int, float]] = 0,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None
):
    ...
```
`Retry` 继承 `TryExcept`，你可以在 `TryExcept` 中找到参数说明，但注意 `Retry` 调用日志记录器的 `warning` 方法。

结合 `TryExcept` 使用，既能重试异常又能处理异常：
```python
from gqylpy_exception import TryExcept, Retry

@TryExcept(ValueError)
@Retry(count=3, cycle=1)
def func():
    int('a')
```
