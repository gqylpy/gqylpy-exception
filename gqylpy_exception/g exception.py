"""
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
import re
import sys
import time
import logging
import asyncio
import warnings
import builtins
import functools
import traceback

from copy import copy, deepcopy

from typing import TypeVar, Type, Optional, Union, Tuple, Callable, Any

Function = Closure = TypeVar('Function', bound=Callable)

ExceptionTypes    = Union[Type[Exception], Tuple[Type[Exception], ...]]
ExceptionLogger   = Union[logging.Logger, 'gqylpy_log']
ExceptionCallback = Callable[[Exception, Function, '...'], None]


class GqylpyError(Exception):
    __module__ = builtins.__name__

    def __init_subclass__(cls) -> None:
        cls.__module__ = builtins.__name__
        setattr(builtins, cls.__name__, cls)

    msg: Any = Exception.args


builtins.GqylpyError = GqylpyError


class MasqueradeClass(type):
    """
    Masquerade one class as another (default masquerade as first parent class).
    Warning, masquerade the class can cause unexpected problems, use caution.
    """
    __module__ = builtins.__name__

    __qualname__ = type.__qualname__
    # Warning, masquerade (modify) this attribute will cannot create the
    # portable serialized representation. In practice, however, this metaclass
    # often does not need to be serialized, so we try to ignore it.

    def __new__(mcs, __name__: str, __bases__: tuple, __dict__: dict):
        __masquerade_class__: Type[object] = __dict__.setdefault(
            '__masquerade_class__', __bases__[0] if __bases__ else object
        )

        if not isinstance(__masquerade_class__, type):
            raise TypeError('"__masquerade_class__" is not a class.')

        cls = type.__new__(
            mcs, __masquerade_class__.__name__, __bases__, __dict__
        )

        if cls.__module__ != __masquerade_class__.__module__:
            setattr(sys.modules[__masquerade_class__.__module__], __name__, cls)

        cls.__realname__   = __name__
        cls.__realmodule__ = cls.__module__
        cls.__module__     = __masquerade_class__.__module__

        # cls.__qualname__ = __masquerade_class__.__qualname__
        # Masquerade (modify) this attribute will cannot create the portable
        # serialized representation. We have not yet found an effective
        # solution, and we will continue to follow up.

        return cls

    def __hash__(cls) -> int:
        if sys._getframe(1).f_code in (deepcopy.__code__, copy.__code__):
            return type.__hash__(cls)
        return hash(cls.__masquerade_class__)

    def __eq__(cls, o) -> bool:
        return True if o is cls.__masquerade_class__ else type.__eq__(cls, o)

    def __init_subclass__(mcs) -> None:
        setattr(builtins, mcs.__name__, mcs)
        mcs.__name__     = MasqueradeClass.__name__
        mcs.__qualname__ = MasqueradeClass.__qualname__
        mcs.__module__   = MasqueradeClass.__module__


MasqueradeClass.__name__ = type.__name__
builtins.MasqueradeClass = MasqueradeClass


class __history__(dict, metaclass=type('SingletonMode', (MasqueradeClass,), {
    '__new__': lambda *a: MasqueradeClass.__new__(*a)()
})):

    def __setitem__(self, *a, **kw) -> None:
        raise __getattr__('ReadOnlyError')('this dictionary is read-only.')

    __delitem__ = setdefault = update = pop = popitem = clear = __setitem__

    def __reduce_ex__(self, protocol: int) -> ...:
        return self.__class__, (dict(self),)

    def copy(self) -> '__history__.__class__':
        return copy(self)


def __getattr__(ename: str, /) -> Union[Type[BaseException], Type[GqylpyError]]:
    if ename in __history__:
        return __history__[ename]

    if ename[:2] == ename[-2:] == '__' and ename[2] != '_' and ename[-3] != '_':
        # Some special modules may attempt to call non-built-in magic method,
        # such as `copy`, `pickle`. Compatible for this purpose.
        raise AttributeError(f'"{__package__}" has no attribute "{ename}".')

    etype = getattr(builtins, ename, None)
    if isinstance(etype, type) and issubclass(etype, BaseException):
        return etype

    if ename[-5:] != 'Error':
        warnings.warn(
            f'strange exception class "{ename}", exception class name should '
            'end with "Error".', stacklevel=2
        )

    etype = type(ename, (GqylpyError,), {})
    dict.__setitem__(__history__, ename, etype)

    return etype


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
        raise ValueError(
            'parameter "logger" must be an instance of "logging.Logger", '
            f'not "{logger.__class__.__name__}".'
        )

    if sys._getframe(2).f_code is Retry.__init__.__code__:
        return logger.warning

    return logger.error


class TryExcept:

    def __init__(
            self,
            etype:      ExceptionTypes,
            /, *,
            silent_exc: bool                        = False,
            raw_exc:    bool                        = False,
            logger:     Optional[ExceptionLogger]   = None,
            ereturn:    Optional[Any]               = None,
            ecallback:  Optional[ExceptionCallback] = None,
            eexit:      bool                        = False
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
                self.core = self.acore
        else:
            if core in (TryExcept.acore, Retry.acore):
                self.core = self.acore

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

    async def acore(self, func: Function, *a, **kw) -> Any:
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

        if isinstance(func, type):
            filepath: str = sys.modules[func.__module__].__file__
        else:
            try:
                filepath: str = func.__globals__['__file__']
            except AttributeError:
                filepath = None

        if filepath is None:
            eline = 'lineX'
        else:
            for line in reversed(einfo.split('\n')[1:-3]):
                if filepath in line:
                    eline: str = re.search(
                        r'line \d+', line
                    ).group().replace(' ', '')
                    break
            else:
                eline = 'lineX'

        return f'[{func.__module__}.{func.__qualname__}.{eline}.' \
               f'{e.__class__.__name__}] {e}'


class Retry(TryExcept):

    def __init__(
            self,
            etype:      ExceptionTypes            = Exception,
            /, *,
            count:      int                       = 0,
            cycle:      int                       = 0,
            silent_exc: bool                      = False,
            raw_exc:    bool                      = False,
            logger:     Optional[ExceptionLogger] = None
    ):
        if not (count.__class__ is int and count >= 0):
            if not (count.__class__ is str and count.isdigit()):
                raise __getattr__('ParameterError')(
                    'parameter "count" must be a positive integer or 0, '
                    f'not "{count}".'
                )
            count = int(count)

        if cycle.__class__ not in (int, float):
            try:
                cycle = float(cycle)
            except (TypeError, ValueError):
                raise __getattr__('ParameterError')(
                    'parameter "cycle" type must be an int or float, '
                    f'not "{cycle.__class__.__name__}".'
                ) from None
        if cycle < 0:
            raise __getattr__('ParameterError')(
                f'parameter "cycle" must be greater than 0, not {cycle}.'
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

    async def acore(self, func: Function, *a, **kw) -> Any:
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
