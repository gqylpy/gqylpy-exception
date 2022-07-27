"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

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
__version__ = 1, 1, 1
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-exception'


def __getattr__(ename: str):
    if ename not in __history__[ename]:
        __history__[ename] = type(ename, (GqylpyError,), {})
    return __history__[ename]


def __getitem__(name: str):
    return __getattr__(name)


__history__: dict
# All the exception classes you've ever created are here.


class GqylpyError(Exception):
    """
    All exception classes created with "gqylpy_exception" inherit from it,
    you can use it to handle any exception created by "gqylpy_exception".
    """


def TryExcept(
        etype:          'Union[type, tuple]',
        *,
        ignore:         'bool'               = None,
        output_raw_exc: 'bool'               = None,
        logger:         'logging.Logger'     = None,
        ereturn:        'Any'                = None,
        ecallback:      'Callable'           = None,
        eexit:          'bool'               = None
):
    """
    "TryExcept" is a decorator, handle exception raised in function decorated.

    @param etype:          Which exceptions to handle.
    @param ignore:         If true, exception are processed silently without output,
                           default false.
    @param output_raw_exc: If true, output the raw exception information directly,
                           default false. Note priority lower than @param(ignore).
    @param logger:         By default, exception information is output to terminal by
                           "sys.stderr". You can specify this parameter, if you want
                           to output exception information using your logger, it will
                           call the logger's "error" method.
    @param ereturn:        If not None, it is returned after an exception is raised.
    @param ecallback:      Receives a callable object and called it after an exception
                           is raised. The callable object receive multiple parameters,
                           raised exception object, function decorated and its arguments.
    @param eexit:          If ture, will exit the program after the exception is
                           triggered, exit code is 4. Default false.

        @TryExcept(ValueError)
        def func():
            int('a')
    """


def Retry(
        etype:          'Union[type, tuple]' = Exception,
        *,
        count:          'int'                = None,
        cycle:          'Union[int, float]'  = None,
        ignore:         'bool'               = None,
        output_raw_exc: 'bool'               = None,
        logger:         'logging.Logger'     = None,
):
    """
    "Retry" is a decorator, when an exception is raised in
    function decorated, attempt to re-execute the function decorated.

    @param etype:          Which exceptions to try.
    @param count:          The retry count, 0 means infinite, default infinite.
    @param cycle:          The retry cycle, default 0.
    @param ignore:         If true, exception are processed silently without output,
                           default false.
    @param output_raw_exc: If true, output the raw exception information directly,
                           default false. Note priority lower than @param(ignore).
    @param logger:         By default, exception information is output to terminal by
                           "sys.stderr". You can specify this parameter, if you want
                           to output exception information using your logger, it will
                           call the logger's "error" method.

    @Retry(count=3, cycle=1)
    def func():
        int('a')

    @TryExcept(ValueError)
    @Retry(count=3, cycle=1)
    def func():
        int('a')
    """


async def TryExceptAsync(
        etype:          'Union[type, tuple]',
        *,
        ignore:         'bool'               = None,
        output_raw_exc: 'bool'               = None,
        logger:         'logging.Logger'     = None,
        ereturn:        'Any'                = None,
        ecallback:      'Callable'           = None,
        eexit:          'bool'               = None
):
    """
    "TryExceptAsync" is a decorator, handle exception raised in asynchronous function decorated.

    @param etype:          Which exceptions to handle.
    @param ignore:         If true, exception are processed silently without output,
                           default false.
    @param output_raw_exc: If true, output the raw exception information directly,
                           default false. Note priority lower than @param(ignore).
    @param logger:         By default, exception information is output to terminal by
                           "sys.stderr". You can specify this parameter, if you want
                           to output exception information using your logger, it will
                           call the logger's "error" method.
    @param ereturn:        If not None, it is returned after an exception is raised.
    @param ecallback:      Receives a callable object and called it after an exception
                           is raised. The callable object receive multiple parameters,
                           raised exception object, function decorated and its arguments.
    @param eexit:          If ture, will exit the program after the exception is
                           triggered, exit code is 4. Default false.

    @TryExceptAsync(ValueError)
    async def func():
        int('a')
    """


async def RetryAsync(
        etype:          'Union[type, tuple]' = Exception,
        *,
        count:          'int'                = None,
        cycle:          'Union[int, float]'  = None,
        ignore:         'bool'               = None,
        output_raw_exc: 'bool'               = None,
        logger:         'logging.Logger'     = None,
):
    """
    "RetryAsync" is a decorator, when an exception is raised in asynchronous
    function decorated, attempt to re-execute the asynchronous function decorated.

    @param etype:          Which exceptions to try.
    @param count:          The retry count, 0 means infinite, default infinite.
    @param cycle:          The retry cycle, default 0.
    @param ignore:         If true, exception are processed silently without output,
                           default false.
    @param output_raw_exc: If true, output the raw exception information directly,
                           default false. Note priority lower than @param(ignore).
    @param logger:         By default, exception information is output to terminal by
                           "sys.stderr". You can specify this parameter, if you want
                           to output exception information using your logger, it will
                           call the logger's "error" method.

    @RetryAsync(count=3, cycle=1)
    async def func():
        int('a')

    @TryExceptAsync(ValueError)
    @RetryAsync(count=3, cycle=1)
    async def func():
        int('a')
    """


class _______歌________琪________怡_______玲_______萍_______云_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname, gvalue in globals().items():
        if gname[0] != '_' and hasattr(gcode, gname):
            gfunc = getattr(gcode, gname)
            gfunc.__module__ = __package__
            setattr(gcode.GqylpyException, gname, gfunc)
        if gname[:2] == '__' and gname != '__builtins__':
            setattr(gcode.GqylpyException, gname, gvalue)

    gcode.GqylpyException.__module__ = __package__
    sys.modules[__name__] = gcode.GqylpyException


import logging
from typing import Any, Union, Callable
