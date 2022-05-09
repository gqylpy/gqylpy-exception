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

Copyright (C) 2022 GQYLPY <http://gqylpy.com>

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
__version__ = 1, 0, 'dev4'
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
        etype: 'Union[type, tuple]',
        *,
        name: str = None,
        ignore: bool = False,
        exc_return: 'Any' = None,
        exc_callback: 'Callable' = None,
        output_full_exc: bool = False,
        exc_exit: bool = False
):
    """Exception handler.
    The function that is decorated will have exception handling capabilities.

    @param etype:               Which exceptions to handle.
    @param name:                Exception identification, which is displayed in the exception output.
    @param ignore:              Whether to ignore an exception or not,
                                if so, no exception information will be logged.
    @param exc_return:          The value returned after the exception was raised.
    @param exc_callback:        The function that is called after the exception is raised.
    @param output_full_exc:     Whether to print the original exception message.
    @param exc_exit:            Exit after an exception is triggered, exit code is 4.

    #-- Example:
        @TryExcept(ValueError)
        def func():
            int('a')
    """


def Retry(
        name: str = None,
        *,
        count: int = None,
        cycle: int = None,
        output_full_exc: bool = False,
        retry_exc: 'Union[type, tuple]' = Exception
):
    """
    When an exception is raised, attempt to re-execute.

    @param name:                Exception identification which is displayed in the exception output.
    @param count:               Total number of executions, default infinite.
    @param cycle:               Seconds between each attempt, default 0.
    @param output_full_exc:     Whether to print the original exception message.
    @param retry_exc:           Which exceptions are supported to retry.

    #-- Example:
        @Retry(count=3, cycle=1)
        def func():
            int('a')

    #-- Use in conjunction with TryExcept will support
        both exception retry and exception handling:
        @TryExcept(ValueError)
        @Retry(count=3, cycle=1)
        def func():
            int('a')
    """


def TryExceptAsync(
        etype: 'Union[type, tuple]',
        *,
        name: str = None,
        ignore: bool = False,
        exc_return: 'Any' = None,
        exc_callback: 'Callable' = None,
        output_full_exc: bool = False
):
    """Exception handler.
    The function that is decorated will have exception handling capabilities.

    @param etype:               Which exceptions to handle.
    @param name:                Exception identification, which is displayed in the exception output.
    @param ignore:              Whether to ignore an exception or not,
                                if so, no exception information will be logged.
    @param exc_return:          The value returned after the exception was raised.
    @param exc_callback:        The function that is called after the exception is raised.
    @param output_full_exc:     Whether to print the original exception message.

    #-- Example:
        @TryExceptAsync(ValueError)
        async def func():
            int('a')
    """


def RetryAsync(
        name: str = None,
        *,
        count: int = None,
        cycle: int = None,
        output_full_exc: bool = False,
        retry_exc: 'Union[type, tuple]' = Exception
):
    """
    When an exception is raised, attempt to re-execute.

    @param name:                Exception identification which is displayed in the exception output.
    @param count:               Total number of executions, default N.
    @param cycle:               Seconds between each attempt, default 0.
    @param output_full_exc:     Whether to print the original exception message.
    @param retry_exc:           Which exceptions are supported to retry.

    #-- Example:
        @RetryAsync(count=3, cycle=1)
        async def func():
            int('a')

    #-- Use in conjunction with TryExcept will support
    both exception retry and exception handling:
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


from typing import Any, Union, Callable
