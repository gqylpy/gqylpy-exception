"""
Create the exception class while executing the `raise` statement, you no longer
need to define an exception class in advance, Convenient and Fast.

    >>> import gqylpy_exception as ge
    >>> raise ge.AnError(...)

    @version: 2.0.1
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-exception

────────────────────────────────────────────────────────────────────────────────
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

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
import warnings

from typing import Type, Optional, Union, Tuple, Dict, Callable, Any

ExceptionTypes    = Union[Type[Exception], Tuple[Type[Exception], ...]]
ExceptionLogger   = Union[logging.Logger, 'gqylpy_log']
ExceptionCallback = Callable[[Exception, Callable, '...'], None]


def __getattr__(ename: str) -> Type['GqylpyError']:
    if ename not in __history__[ename]:
        __history__[ename] = type(ename, (GqylpyError,), {})
    return __history__[ename]


def __getitem__(ename: str) -> Type['GqylpyError']:
    return __getattr__(ename)


__history__: Dict[str, Type['GqylpyError']]
# All the exception classes you've ever created are here.


class GqylpyError(Exception):
    """
    All exception classes created with `gqylpy_exception` inherit from it, you
    can use it to handle any exception created by `gqylpy_exception`.
    """
    msg: Any


def TryExcept(
        etype:      ExceptionTypes,
        *,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ereturn:    Optional[Any]               = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
) -> Callable:
    """
    `TryExcept` is a decorator (is an additional function of `gqylpy_exception`
    ), handles exceptions raised by the function it decorates.

        >>> @TryExcept(ValueError)
        >>> def func():
        >>>    int('a')

    @param etype:      Which exceptions to handle.
    @param silent_exc: If true, exception are processed silently without output,
                       default False.
    @param raw_exc:    If true, output the raw exception information directly,
                       default False. Note priority lower than parameter
                       `silent_exc`.
    @param logger:     By default, exception information is output to terminal
                       by `sys.stderr`. You can specify this parameter, if you
                       want to output exception information using your logger,
                       it will call the logger's `error` method.
    @param ereturn:    If not None, it is returned after an exception is raised.
    @param ecallback:  Receives a callable object and called it after an
                       exception is raised. The callable object receive multiple
                       parameters, raised exception object, function decorated
                       and its arguments.
    @param eexit:      If ture, will exit the program after the exception is
                       triggered, exit code is 4. Default false.
    """


def Retry(
        etype:      Optional[ExceptionTypes]    = None,
        *,
        count:      Optional[int]               = None,
        cycle:      Optional[Union[int, float]] = None,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None
) -> Callable:
    """
    `Retry` is a decorator (is an additional function of `gqylpy_exception`),
    retries exceptions raised by the function it decorates. When an exception is
    raised in function decorated, try to re-execute the function decorated.

        >>> @Retry(count=3, cycle=1)
        >>> def func():
        >>>     int('a')

        >>> @TryExcept(ValueError)
        >>> @Retry(count=3, cycle=1)
        >>> def func():
        >>>     int('a')

    @param etype:      Which exceptions to retry, default try all exceptions to
                       `Exception` and its subclasses.
    @param count:      The retry count, 0 means infinite, default infinite.
    @param cycle:      The retry cycle, default 0.
    @param silent_exc: If true, exception are processed silently without output,
                       default False.
    @param raw_exc:    If true, output the raw exception information directly,
                       default False. Note priority lower than parameter
                       `silent_exc`.
    @param logger:     By default, exception information is output to terminal
                       by `sys.stderr`. You can specify this parameter, if you
                       want to output exception information using your logger,
                       it will call the logger's `warning` method.
    """


async def TryExceptAsync(
        etype:      Union[ExceptionTypes],
        *,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ereturn:    Optional[Any]               = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
) -> Callable:
    """`TryExceptAsync` is a decorator (is an additional function of
    `gqylpy_exception`), handles exceptions raised by the asynchronous function
    it decorates."""
    warnings.warn(
        f'will be deprecated soon, replaced to {TryExcept}.', DeprecationWarning
    )
    return TryExcept(
        etype,
        silent_exc=silent_exc,
        raw_exc   =raw_exc,
        logger    =logger,
        ereturn   =ereturn,
        ecallback =ecallback,
        eexit     =eexit
    )


async def RetryAsync(
        etype:      Optional[ExceptionTypes]    = None,
        *,
        count:      Optional[int]               = None,
        cycle:      Optional[Union[int, float]] = None,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None
) -> Callable:
    """`RetryAsync` is a decorator (is an additional function of
    `gqylpy_exception`), retries exceptions raised by the asynchronous function
    it decorates."""
    warnings.warn(
        f'will be deprecated soon, replaced to {Retry}.', DeprecationWarning
    )
    return Retry(
        etype,
        count     =count,
        cycle     =cycle,
        silent_exc=silent_exc,
        raw_exc   =raw_exc,
        logger    =logger
    )


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    gpath = f'{__name__}.g {__name__[7:]}'
    __import__(gpath)

    gcode = globals()[f'g {__name__[7:]}']
    ge = gcode.GqylpyException()

    for gname in globals():
        if gname[0] == '_':
            setattr(ge, gname, globals()[gname])
        else:
            try:
                gfunc = getattr(gcode, gname)
                assert gfunc.__module__ in (gpath, __package__)
            except (AttributeError, AssertionError):
                continue
            gfunc.__module__ = __package__
            setattr(ge, gname, gfunc)

    ge.__module__ = __package__
    sys.modules[__name__] = ge.GqylpyException = ge
