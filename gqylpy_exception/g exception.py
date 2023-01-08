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


class GqylpyException:
    __history__ = {}

    def __getattr__(self, ename: str) -> type:
        try:
            eclass = self.__history__[ename]
        except KeyError:
            if hasattr(builtins, ename):
                raise self.ExceptionClassIsBuiltinsError(
                    f'exception class "{ename}" is builtins.'
                )
            # Some special modules may attempt to call non-built-in magic
            # method, such as `copy`, `pickle`. Compatible for this purpose.
            if ename[:2] == ename[-2:] == '__' and \
                    ename[2] != '_' and ename[-3] != '_':
                raise AttributeError(
                    f'"{__package__}" has no attribute "{ename}"'
                )
            if ename[-5:] != 'Error':
                warnings.warn(
                    message=f'strange exception class "{ename}", exception '
                        'class name should end with "Error".',
                    category=type('ImproperUseWarning', (Warning,), {})
                )
            eclass = self.__history__[ename] = type(
                ename, (self.GqylpyError,), {'__module__': 'builtins'}
            )
            # Compatible with object serialization.
            setattr(builtins, ename, eclass)
        return eclass

    def __getitem__(self, ename: str) -> type:
        return getattr(self, ename)

    class GqylpyError(Exception):
        __module__ = 'builtins'

        @property
        def msg(self):
            args_length: int = len(self.args)
            if args_length == 0:
                return ''
            if args_length == 1:
                return self.args[0]
            return self.args


# Compatible with object serialization, for `GqylpyException.GqylpyError`.
builtins.GqylpyException = GqylpyException


class TryExcept:

    def __init__(
            self,
            etype:          [type, tuple],
            *,
            ignore:         bool          = False,
            output_raw_exc: bool          = False,
            logger:         ...           = None,
            ereturn:        ...           = None,
            ecallback:      ...           = None,
            eexit:          bool          = False
    ):
        self.etype          = etype
        self.ignore         = ignore
        self.output_raw_exc = output_raw_exc
        self.logger         = logger
        self.ereturn        = ereturn
        self.ecallback      = ecallback
        self.eexit          = eexit

    def __call__(self, func):
        @functools.wraps(func, updated=('__dict__', '__globals__'))
        def inner(*a, **kw):
            return self.core(func, *a, **kw)
        return inner

    def core(self, func, *a, **kw):
        try:
            return func(*a, **kw)
        except self.etype as e:
            self.exception_handling(func, e, *a, **kw)
        return self.ereturn

    def exception_handling(self, func, e: Exception, *a, **kw):
        local_instance: bool = self.__class__ in (TryExcept, TryExceptAsync)

        if not self.ignore:
            try:
                einfo: str = self.exception_analysis(func, e)
            except Exception as ee:
                einfo: str = f'{self.__class__.__name__}Error: {ee}'

            if not local_instance:
                einfo: str = f'[try:{kw["count"]}/{self.count}:{self.cycle}] ' \
                             f'{einfo}'

            if self.logger:
                if not(
                        isinstance(self.logger, logging.Logger) or
                        getattr(self.logger, '__name__', None) == 'gqylpy_log'
                ):
                    x: str = self.logger.__class__.__name__
                    raise GqylpyException.ParameterError(
                        f'parameter "logger" must be an instance '
                        f'of "logging.Logger", not "{x}".'
                    )
                (self.logger.error if local_instance else self.logger.warning)(
                    einfo, stacklevel=4 if local_instance else 6)
            else:
                now: str = time.strftime('%F %T', time.localtime())
                sys.stderr.write(f'[{now}] {einfo}\n')

        if local_instance:
            self.ecallback and self.ecallback(e, func, *a, **kw)
            self.eexit and exit(4)

    def exception_analysis(self, func, e: Exception) -> str:
        einfo: str = traceback.format_exc()

        if self.output_raw_exc:
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
            etype:          [type, tuple] = Exception,
            *,
            count:          int           = 0,
            cycle:          int           = 0,
            ignore:         bool          = False,
            output_raw_exc: bool          = False,
            logger:         ...           = None,
    ):
        if not (count.__class__ is int and count >= 0):
            if not (count.__class__ is str and count.isdigit()):
                raise GqylpyException.ParameterError(
                    'parameter "count" must be a '
                    f'positive integer or 0, not "{count}".'
                )
            count = int(count)

        if cycle.__class__ not in (int, float):
            try:
                cycle = float(cycle)
            except (TypeError, ValueError):
                raise GqylpyException.ParameterError(
                    'parameter "cycle" must be a '
                    f'positive number or 0, not "{cycle}"'
                )
        if cycle < 0:
            raise GqylpyException.ParameterError(
                'parameter "cycle" must be a '
                f'positive number or 0, not "{cycle}"'
            )

        self.count = count or 'N'
        self.cycle = cycle

        super().__init__(
            etype,
            ignore=ignore,
            output_raw_exc=output_raw_exc,
            logger=logger
        )

    def core(self, func, *a, **kw):
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


class TryExceptAsync(TryExcept):

    async def core(self, func, *a, **kw):
        try:
            return await func(*a, **kw)
        except self.etype as e:
            self.exception_handling(func, e, *a, **kw)
        return self.ereturn


class RetryAsync(Retry):

    async def core(self, func, *a, **kw):
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
