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
import os
import re
import time
import warnings
import functools
import traceback

import gqylpy_log as glog


class ObjectMode(type):

    def __new__(mcs, cls, bases, attrs):
        return super().__new__(mcs, cls, bases, attrs)()


class GqylpyError(Exception):
    __module__ = 'E'


class GqylpyException(metaclass=ObjectMode):
    history = {}

    def __getattribute__(self, name: str) -> type:
        if name[:2] == name[-2:] == '__':
            return

        if name == 'history':
            return super().__getattribute__(name)

        if name in self.history:
            return self.history[name]

        if name == 'GqylpyError':
            return GqylpyError
        if name == 'Retry':
            return Retry

        if name[-5:] != 'Error':
            msg = f'Strange exception class: "{name}", ' \
                  f'exception class name should end with "Error".'
            warnings.warn(msg)

        eclass = type(name, (GqylpyError,), {'__module__': 'E'})
        self.history[name] = eclass

        return eclass

    def __getitem__(self, name: str) -> type:
        return getattr(self, name)


class TryExcept:

    __module__ = __name__[:16]

    def __init__(
            self,
            etype: type or tuple,
            *,
            name: str = None,
            ignore: bool = False,
            exc_return=None,
            exc_callback=None,
            output_full_exc: bool = False,
            exc_exit: bool = False,
    ):
        self.etype = etype
        self.name = name
        self.ignore = ignore
        self.exc_return = exc_return
        self.exc_callback = exc_callback
        self.output_full_exc = output_full_exc
        self.exc_exit = exc_exit

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*a, **kw):
            return self.core(func, *a, **kw)
        return inner

    def core(self, func, *a, **kw):
        try:
            return func(*a, **kw)
        except self.etype as e:
            self.exception_handler(func, e, *a, **kw)
            if self.exc_exit:
                os._exit(4)
        return self.exc_return

    def exception_handler(self, func, e: Exception, *a, **kw):
        if self.ignore:
            return

        try:
            glog.error(self.analysis_exception(func, e))
        except Exception as ee:
            glog.error(f'TryExceptError: {ee}')

        if self.exc_callback:
            return self.exc_callback(*a, **kw)

    def analysis_exception(self, func, e: Exception) -> str:
        einfo: str = traceback.format_exc()

        if self.output_full_exc:
            return einfo

        func_name: str = func.__qualname__
        module_name: str = func.__module__
        efile: str = func.__globals__['__file__']

        name: str = self.name or f'{module_name}.{func_name}'
        ename: str = type(e).__name__

        for line in reversed(einfo.split('\n')[1:-3]):
            if efile in line:
                eline: str = re.search(
                    r'line \d+', line).group().replace(' ', '')
                break
        else:
            eline: str = 'lineX'

        return f'[{name}.{eline}.{ename}] {e}'


class Retry:

    __module__ = __name__[:16]

    def __init__(
            self,
            name: str = None,
            *,
            count: int = 'N',
            cycle: int = 0,
            output_full_exc: bool = False,
            retry_exc: type or tuple = Exception
    ):
        self.name = name
        self.count = count
        self.cycle = cycle
        self.output_full_exc = output_full_exc
        self.retry_exc = retry_exc

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*a, **kw):
            return self.core(func, *a, **kw)
        return inner

    def core(self, func, *a, **kw):
        count = 0

        while True:
            try:
                return func(*a, **kw)
            except self.retry_exc as e:
                count += 1

                try:
                    einfo: str = TryExcept.analysis_exception(self, func, e)
                    glog.warning(f'[try:{count}/{self.count}] {einfo}')
                except Exception as ee:
                    glog.error(f'RetryError: {ee}')

                if count == self.count:
                    raise e

            time.sleep(self.cycle)
