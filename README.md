[<img alt="LOGO" src="http://gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-exception.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-exception/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_exception)](https://pypi.org/project/gqylpy_exception)
[![License](https://img.shields.io/pypi/l/gqylpy_exception)](https://github.com/gqylpy/gqylpy-exception/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/gqylpy_exception)](https://pepy.tech/project/gqylpy_exception)

# gqylpy-exception
English | [中文](https://github.com/gqylpy/gqylpy-exception/blob/master/README_CN.md)

Raise exceptions while creating exception classes on the fly, without the need to predefine them beforehand. For instance, if you want to raise an exception named `NotUnderstandError`, simply import `import gqylpy_exception as ge` and execute `raise ge.NotUnderstandError` directly for convenience and efficiency.

<kbd>pip3 install gqylpy_exception</kbd>

###### Using `gqylpy_exception` to Create Exception Classes

```python
import gqylpy_exception as ge

raise ge.AnError(...)
```

With `gqylpy_exception`, you can create exception classes with arbitrary names. `AnError` is not predefined in `gqylpy_exception`; it is dynamically created when your code executes `ge.` due to the magic method `__getattr__`.

Alternatively, you can also create exceptions upon import:

```python
from gqylpy_exception import AnError

raise AnError(...)
```

Lastly, `gqylpy_exception` avoids duplicate creation of exception classes. Once an exception class has been created, it is stored in the `ge.__history__` dictionary. When you attempt to create the same exception again, it will be retrieved from this dictionary.
