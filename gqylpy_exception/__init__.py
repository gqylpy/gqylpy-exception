"""
`gqylpy-exception` is a flexible and convenient Python exception handling
library that allows you to dynamically create exception classes and provides
various exception handling mechanisms.

    >>> # Dynamically Creating Exceptions.
    >>> import gqylpy_exception as ge
    >>> raise ge.AnError(...)

    >>> # Powerful Exception Handling Capabilities.
    >>> from gqylpy_exception import TryExcept, Retry, TryContext

    >>> @TryExcept(ValueError)
    >>> def func():
    >>>     int('a')

    >>> @Retry(count=3, cycle=1)
    >>> def func():
    >>>     int('a')

    >>> with TryContext(ValueError):
    >>>     int('a')

    @version: 3.1.1
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-exception

────────────────────────────────────────────────────────────────────────────────
Copyright (c) 2022-2024 GQYLPY <http://gqylpy.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

from typing import Type, Optional, Union, Tuple, Dict, Callable, Any

ExceptionTypes    = Union[Type[Exception], Tuple[Type[Exception], ...]]
ExceptionLogger   = Union[logging.Logger, 'gqylpy_log']
ExceptionCallback = Callable[[Exception, Callable, '...'], None]


class GqylpyError(Exception):
    """
    All exception classes created with `gqylpy_exception` inherit from it, you
    can use it to handle any exception created by `gqylpy_exception`.
    """
    msg: Any = Exception.args


__history__: Dict[str, Type[GqylpyError]]
# All the exception classes you've ever created are here.
# This dictionary is read-only.


def __getattr__(ename: str, /) -> Type[GqylpyError]:
    """
    Create an exception type called `ename` and return it.

    The created exception type will be stored to the dictionary `__history__`,
    and when you create an exception type with the same name again, directly get
    the value from this dictionary, rather than being created repeatedly.

    For Python built-in exception types, returned directly, are not repeatedly
    creation, and not stored to dictionary `__history__`.
    """
    return __history__.setdefault(ename, type(ename, (GqylpyError,), {}))


def TryExcept(
        etype:      ExceptionTypes,
        /, *,
        silent:     Optional[bool]              = None,
        raw:        Optional[bool]              = None,
        last_tb:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ereturn:    Optional[Any]               = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
) -> Callable:
    """
    `TryExcept` is a decorator that handles exceptions raised by the function it
    decorates.

        >>> @TryExcept(ValueError)
        >>> def func():
        >>>    int('a')

    @param etype:
        The types of exceptions to be handled, multiple types can be passed in
        using a tuple.

    @param silent:
        If True, exceptions will be silently handled without any output.
        Defaults to False.

    @param raw:
        If True, raw exception information will be directly output. Defaults to
        False. Note that its priority is lower than the `silent` parameter.

    @param last_tb:
        Whether to trace to the last traceback object of the exception. Defaults
        to False, tracing only to the current code segment.

    @param logger:
        By default, exception information is output to the terminal via
        `sys.stderr`. If you want to use your own logger to record exception
        information, you can pass the logger to this parameter, and the `error`
        method of the logger will be called internally.

    @param ereturn:
        The value to be returned when the decorated function raises an
        exception. Defaults to None.

    @param ecallback:
        Accepts a callable object and invokes it when an exception is raised.
        The callable object takes one argument, the raised exception object.

    @param eexit:
        If True, the program will execute `raise SystemExit(4)` and exit after
        an exception is raised, with an exit code of 4. If the ecallback
        parameter is provided, the program will execute the callback function
        first before exiting. Defaults to False.
    """


def Retry(
        etype:   Optional[ExceptionTypes]    = None,
        /, *,
        count:   Optional[int]               = None,
        cycle:   Optional[Union[int, float]] = None,
        silent:  Optional[bool]              = None,
        raw:     Optional[bool]              = None,
        last_tb: Optional[bool]              = None,
        logger:  Optional[ExceptionLogger]   = None
) -> Callable:
    """
    `Retry` is a decorator that retries exceptions raised by the function it
    decorates. When an exception is raised in the decorated function, it
    attempts to re-execute the decorated function based on the parameters
    `count` and `cycle`.

        >>> @Retry(count=3, cycle=1)
        >>> def func():
        >>>     int('a')

        >>> @TryExcept(ValueError)
        >>> @Retry(count=3, cycle=1)
        >>> def func():
        >>>     int('a')

    @param etype:
        The types of exceptions to be handled, multiple types can be specified
        by passing them in a tuple. The default is `Exception`.

    @param count:
        The number of retries, 0 means infinite retries, infinite by default.

    @param cycle:
        Retry cycle (time between retries), with a default of 0 seconds.

    @param silent:
        If True, exceptions will be silently handled without any output.
        Defaults to False.

    @param raw:
        If True, raw exception information will be directly output. Defaults to
        False. Note that its priority is lower than the `silent` parameter.

    @param last_tb:
        Whether to trace to the last traceback object of the exception. Defaults
        to False, tracing only to the current code segment.

    @param logger:
        By default, exception information is output to the terminal via
        `sys.stderr`. If you want to use your own logger to record exception
        information, you can pass the logger to this parameter, and the `error`
        method of the logger will be called internally.
    """


async def TryExceptAsync(etype: ExceptionTypes, /, **kw) -> Callable:
    """`TryExcept` is a decorator that handles exceptions raised by the
    asynchronous function it decorates."""
    warnings.warn(
        f'will be deprecated soon, replaced to {TryExcept}.', DeprecationWarning
    )
    return TryExcept(etype, **kw)


async def RetryAsync(
        etype: ExceptionTypes              = None,
        /, *,
        count: Optional[int]               = None,
        cycle: Optional[Union[int, float]] = None,
        **kw
) -> Callable:
    """`Retry` is a decorator that retries exceptions raised by the asynchronous
    function it decorates. When an exception is raised in the decorated
    asynchronous function, it attempts to re-execute the decorated asynchronous
    function based on the parameters `count` and `cycle`."""
    warnings.warn(
        f'will be deprecated soon, replaced to {Retry}.', DeprecationWarning
    )
    return Retry(etype, count=count, cycle=cycle, **kw)


def TryContext(
        etype:      ExceptionTypes,
        /, *,
        silent:     Optional[bool]              = None,
        raw:        Optional[bool]              = None,
        last_tb:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
) -> None:
    """
    TryContext is a context manager that handles exceptions raised within the
    context.

        >>> with TryContext(ValueError):
        >>>     int('a')

    @param etype:
        The types of exceptions to be handled, multiple types can be passed in
        using a tuple.

    @param silent:
        If True, exceptions will be silently handled without any output.
        Defaults to False.

    @param raw:
        If True, raw exception information will be directly output. Defaults to
        False. Note that its priority is lower than the `silent` parameter.

    @param last_tb:
        Whether to trace to the last traceback object of the exception. Defaults
        to False, tracing only to the current code segment.

    @param logger:
        By default, exception information is output to the terminal via
        `sys.stderr`. If you want to use your own logger to record exception
        information, you can pass the logger to this parameter, and the `error`
        method of the logger will be called internally.

    @param ecallback:
        Accepts a callable object and invokes it when an exception is raised.
        The callable object takes one argument, the raised exception object.

    @param eexit:
        If True, the program will execute `raise SystemExit(4)` and exit after
        an exception is raised, with an exit code of 4. If the ecallback
        parameter is provided, the program will execute the callback function
        first before exiting. Defaults to False.
    """


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    if sys.platform != 'linux' or \
            logging.__file__[:-20] == __file__[:-len(__name__) - 27]:

        gpack = globals()
        gpath = f'{__name__}.g {__name__[7:]}'
        gcode = __import__(gpath, fromlist=...)

        gpack['GqylpyError'] = gcode.GqylpyError
        gpack['__history__'] = gcode.__history__

        for gname in gcode.__dir__():
            gfunc = getattr(gcode, gname)
            if gname in gpack and getattr(gfunc, '__module__', None) == gpath:
                gfunc.__module__ = __package__
                gfunc.__doc__ = gpack[gname].__doc__
                gpack[gname] = gfunc

        gpack['TryExceptAsync'] = gpack['TryExcept']
        gpack['RetryAsync']     = gpack['Retry']
