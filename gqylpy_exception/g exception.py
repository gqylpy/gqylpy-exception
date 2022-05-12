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
import logging
import os
import re
import time
import asyncio
import warnings
import functools
import traceback

import gqylpy_log as glog


class GqylpyException(metaclass=type(
    'SingletonMode', (type,),
    {'__new__': lambda *a: type.__new__(*a)()}
)):
    __history__ = {}

    def __getattr__(self, ename: str) -> type:
        try:
            eclass = self.__history__[ename]
        except KeyError:
            if ename[-5:] != 'Error':
                warnings.warn(
                    f'Strange exception class "{ename}", exception '
                    f'class name should end with "Error".'
                )
            eclass = self.__history__[ename] = type(
                ename, (self.GqylpyError,),
                {'__module__': self.GqylpyError.__module__}
            )
        return eclass

    def __getitem__(self, ename: str) -> type:
        return getattr(self, ename)

    class GqylpyError(Exception):
        __module__ = 'E'


class TryExcept:

    def __init__(
            self,
            etype: type or tuple,
            *,
            name: str = None,
            ereturn=None,
            ecallback=None,
            eignore: bool = False,
            eintact: bool = False,
            eexit: bool = False,
            elogger: logging.Logger = None
    ):
        self.etype = etype
        self.name = name
        self.ignore = eignore
        self.ereturn = ereturn
        self.ecallback = ecallback
        self.eintact = eintact
        self.eexit = eexit

        self.logger = elogger or glog.__init__(
            __package__,
            level=glog.WARNING,
            output='stream',
            logfmt='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%F %T',
            gname=__package__
        )

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*a, **kw):
            return self.core(func, *a, **kw)
        return inner

    def core(self, func, *a, **kw):
        try:
            return func(*a, **kw)
        except self.etype as e:
            self.exception_handling(func, e, *a, **kw)
            self.eexit and exit(4)
        return self.ereturn

    def exception_handling(self, func, e: Exception, *a, **kw):
        if self.ignore:
            return

        try:
            self.logger.error(self.exception_analysis(func, e))
        except Exception as ee:
            self.logger.error(f'TryExceptError: {ee}')

        if self.ecallback:
            return self.ecallback(*a, **kw)

    def exception_analysis(self, func, e: Exception) -> str:
        einfo: str = traceback.format_exc()

        if self.eintact:
            return einfo

        module: str = func.__module__
        funcname: str = func.__qualname__
        efile: str = func.__globals__['__file__']

        name: str = self.name or f'{module}.{funcname}'
        ename: str = type(e).__name__

        for line in reversed(einfo.split('\n')[1:-3]):
            if efile in line:
                eline: str = re.search(
                    r'line \d+', line).group().replace(' ', '')
                break
        else:
            eline: str = 'lineX'

        return f'[{name}.{eline}.{ename}] {e}'


class Retry(TryExcept):

    def __init__(
            self,
            name: str = None,
            *,
            count: int = 'N',
            cycle: int = 0,
            eintact: bool = False,
            retry_exc: type or tuple = Exception
    ):
        self.name = name
        self.count = count
        self.cycle = cycle
        self.eintact = eintact
        self.retry_exc = retry_exc

    def core(self, func, *a, **kw):
        count = 0

        while True:
            try:
                return func(*a, **kw)
            except self.retry_exc as e:
                count += 1

                try:
                    einfo: str = self.exception_analysis(func, e)
                    self.logger.warning(f'[try:{count}/{self.count}] {einfo}', stacklevel=5)
                except Exception as ee:
                    self.logger.error(f'RetryError: {ee}')

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
            except self.retry_exc as e:
                count += 1

                try:
                    einfo: str = self.exception_analysis(func, e)
                    self.logger.warning(f'[try:{count}/{self.count}] {einfo}')
                except Exception as ee:
                    self.logger.error(f'RetryError: {ee}')

                if count == self.count:
                    raise e

            await asyncio.sleep(self.cycle)
