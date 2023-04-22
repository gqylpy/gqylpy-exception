"""
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
import re
import sys
import time
import logging
import asyncio
import warnings
import builtins
import functools
import traceback

from typing import TypeVar, Type, Optional, Union, Tuple, Callable, Any

Function = Closure = TypeVar('Function', bound=Callable)

ExceptionTypes    = Union[Type[Exception], Tuple[Type[Exception], ...]]
ExceptionLogger   = Union[logging.Logger, 'gqylpy_log']
ExceptionCallback = Callable[[Exception, Function, '...'], None]

warnings.filterwarnings('once', category=DeprecationWarning)


class GqylpyException:
    __history__ = {}

    def __getattr__(self, ename: str) -> Type['GqylpyError']:
        try:
            eclass = self.__history__[ename]
        except KeyError:
            if hasattr(builtins, ename):
                raise self.ExceptionClassIsBuiltinsError(
                    f'exception class "{ename}" is builtins.'
                ) from None
            # Some special modules may attempt to call non-built-in magic
            # method, such as `copy`, `pickle`. Compatible for this purpose.
            if ename[:2] == ename[-2:] == '__' and \
                    ename[2] != '_' and ename[-3] != '_':
                raise AttributeError(
                    f'"{__package__}" has no attribute "{ename}".'
                ) from None
            if ename[-5:] != 'Error':
                warnings.warn(
                    f'strange exception class "{ename}", exception class name '
                    'should end with "Error".', UserWarning, stacklevel=2
                )
            eclass = self.__history__[ename] = type(
                ename, (self.GqylpyError,), {'__module__': 'builtins'}
            )
            # Compatible with object serialization.
            setattr(builtins, ename, eclass)
        return eclass

    def __getitem__(self, ename: str) -> Type['GqylpyError']:
        return getattr(self, ename)

    class GqylpyError(Exception):
        __module__ = 'builtins'

        @property
        def msg(self) -> Any:
            return self.args[0] if len(self.args) == 1 else \
                self.args if self.args else None

# Compatible with object serialization, for `GqylpyException.GqylpyError`.
builtins.GqylpyException = GqylpyException


def stderr(einfo: str) -> None:
    now: str = time.strftime('%F %T', time.localtime())
    sys.stderr.write(f'[{now}] {einfo}\n')


def get_logger(logger: logging.Logger) -> Callable[[str], None]:
    if logger is None:
        return stderr

    if not (
            isinstance(logger, logging.Logger) or
            getattr(logger, '__package__', None) == 'gqylpy_log'
    ):
        raise ParameterError(
            'parameter "logger" must be an instance of "logging.Logger", '
            f'not "{logger.__class__.__name__}".'
        )

    if sys._getframe(2).f_code is Retry.__init__.__code__:
        return logger.warning

    return logger.error


class TryExcept:

    def __new__(cls, *a, **kw):
        if 'ignore' in kw:
            warnings.warn(DeprecationWarning(
                'parameter "ignore" deprecated, replaced to "silent_exc".'
            ), stacklevel=2)
        if 'output_raw_exc' in kw:
            warnings.warn(DeprecationWarning(
                'parameter "output_raw_exc" deprecated, replaced to "raw_exc".'
            ), stacklevel=2)
        return object.__new__(cls)

    def __init__(
            self,
            etype:      ExceptionTypes,
            *,
            silent_exc: bool                        = False,
            raw_exc:    bool                        = False,
            logger:     Optional[ExceptionLogger]   = None,
            ereturn:    Optional[Any]               = None,
            ecallback:  Optional[ExceptionCallback] = None,
            eexit:      bool                        = False,
            ignore         = None,
            output_raw_exc = None
    ):
        self.etype      = etype
        self.silent_exc = silent_exc
        self.raw_exc    = raw_exc
        self.logger     = get_logger(logger)
        self.ereturn    = ereturn
        self.ecallback  = ecallback
        self.eexit      = eexit

        self.local: bool = self.__class__ is TryExcept

    def __call__(self, func: Function) -> Closure:
        try:
            core = func.__closure__[1].cell_contents.core.__func__
        except (TypeError, IndexError, AttributeError):
            if asyncio.iscoroutinefunction(func):
                self.core = self.core_async
        else:
            if core in (TryExcept.core_async, Retry.core_async):
                self.core = self.core_async

        @functools.wraps(func, updated=('__dict__', '__globals__'))
        def inner(*a, **kw) -> Any:
            return self.core(func, *a, **kw)

        return inner

    def core(self, func: Function, *a, **kw) -> Any:
        try:
            return func(*a, **kw)
        except self.etype as e:
            self.exception_handling(func, e, *a, **kw)
        return self.ereturn

    async def core_async(self, func: Function, *a, **kw) -> Any:
        try:
            return await func(*a, **kw)
        except self.etype as e:
            self.exception_handling(func, e, *a, **kw)
        return self.ereturn

    def exception_handling(
            self, func: Function, e: Exception, *a, **kw
    ) -> None:
        if not self.silent_exc:
            try:
                einfo: str = self.exception_analysis(func, e)
            except Exception as ee:
                einfo: str = f'{self.__class__.__name__}Error: {ee}'
            if not self.local:
                einfo = f'[try:{kw["count"]}/{self.count}:{self.cycle}] {einfo}'
            self.logger(einfo)

        if self.local:
            if self.ecallback:
                self.ecallback(e, func, *a, **kw)
            if self.eexit:
                raise SystemExit(4)

    def exception_analysis(self, func: Function, e: Exception) -> str:
        einfo: str = traceback.format_exc()

        if self.raw_exc:
            return einfo

        filepath: str = func.__globals__['__file__']
        funcpath: str = f'{func.__module__}.{func.__qualname__}'

        for line in reversed(einfo.split('\n')[1:-3]):
            if filepath in line:
                eline: str = re.search(
                    r'line \d+', line
                ).group().replace(' ', '')
                break
        else:
            eline: str = 'lineX'

        return f'[{funcpath}.{eline}.{e.__class__.__name__}] {e}'


class Retry(TryExcept):

    def __init__(
            self,
            etype:      ExceptionTypes            = Exception,
            *,
            count:      int                       = 0,
            cycle:      int                       = 0,
            silent_exc: bool                      = False,
            raw_exc:    bool                      = False,
            logger:     Optional[ExceptionLogger] = None,
            ignore         = None,
            output_raw_exc = None
    ):
        if not (count.__class__ is int and count >= 0):
            if not (count.__class__ is str and count.isdigit()):
                raise ParameterError(
                    'parameter "count" must be a positive integer or 0, '
                    f'not "{count}".'
                )
            count = int(count)

        if cycle.__class__ not in (int, float):
            try:
                cycle = float(cycle)
            except (TypeError, ValueError):
                raise ParameterError(
                    'parameter "count" must be a positive integer or 0, '
                    f'not "{count}".'
                ) from None
        if cycle < 0:
            raise ParameterError(
                'parameter "count" must be a positive integer or 0, '
                f'not "{count}".'
            )

        self.count = count or 'N'
        self.cycle = cycle

        TryExcept.__init__(
            self, etype, silent_exc=silent_exc, raw_exc=raw_exc, logger=logger
        )

    def core(self, func: Function, *a, **kw) -> Any:
        count = 0

        while True:
            try:
                return func(*a, **kw)
            except self.etype as e:
                count += 1
                self.exception_handling(func, e, count=count)
                if count == self.count:
                    raise e

            time.sleep(self.cycle)

    async def core_async(self, func: Function, *a, **kw) -> Any:
        count = 0

        while True:
            try:
                return await func(*a, **kw)
            except self.etype as e:
                count += 1
                self.exception_handling(func, e, count=count)
                if count == self.count:
                    raise e

            await asyncio.sleep(self.cycle)


TryExceptAsync, RetryAsync = TryExcept, Retry

ParameterError = GqylpyException().ParameterError
