[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-exception.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-exception/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_exception)](https://pypi.org/project/gqylpy_exception)
[![License](https://img.shields.io/pypi/l/gqylpy_exception)](https://github.com/gqylpy/gqylpy-exception/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_exception/month)](https://pepy.tech/project/gqylpy_exception)

# gqylpy-exception


> 在执行 `raise` 语句的同时创建异常类，无需事先定义异常类，方便快捷。例如，你想抛出一个名为 `NotUnderstandError` 的异常，
> 导入 `import gqylpy_exception as ge` 后直接执行 `raise ge.NotUnderstandError` 即可。

<kbd>pip3 install gqylpy_exception</kbd>


###### 使用 `gqylpy_exception` 创建异常类
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
