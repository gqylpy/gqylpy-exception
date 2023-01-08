"""
Create the exception class while executing the `raise` statement, you no longer
need to define an exception class in advance, Convenient and Fast.

    >>> import gqylpy_exception as ge
    >>> raise ge.AnError(...)

    @version: 1.3.2
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


def __getattr__(ename: str) -> type:
    if ename not in __history__[ename]:
        __history__[ename] = type(ename, (GqylpyError,), {})
    return __history__[ename]


def __getitem__(name: str) -> type:
    return __getattr__(name)


__history__: dict
# All the exception classes you've ever created are here.


class GqylpyError(Exception):
    """
    All exception classes created with `gqylpy_exception` inherit from it, you
    can use it to handle any exception created by `gqylpy_exception`.
    """
    msg: 'Any'


def TryExcept(
        etype:          'Union[type, Tuple[type, ...]]',
        *,
        ignore:         'bool'                                       = None,
        output_raw_exc: 'bool'                                       = None,
        logger:         'logging.Logger'                             = None,
        ereturn:        'Any'                                        = None,
        ecallback:      'Callable[[Exception, Callable, ...], None]' = None,
        eexit:          'bool'                                       = None
) -> 'Callable':
    """
    `TryExcept` is a decorator, handle exception raised in function decorated.

    @param etype:          Which exceptions to handle.
    @param ignore:         If true, exception are processed silently without
                           output, default false.
    @param output_raw_exc: If true, output the raw exception information
                           directly, default false. Note priority lower than
                           parameter `ignore`.
    @param logger:         By default, exception information is output to
                           terminal by `sys.stderr`. You can specify this
                           parameter, if you want to output exception
                           information using your logger, it will call the
                           logger's `error` method.
    @param ereturn:        If not None, it is returned after an exception is
                           raised.
    @param ecallback:      Receives a callable object and called it after an
                           exception is raised. The callable object receive
                           multiple parameters, raised exception object,
                           function decorated and its arguments.
    @param eexit:          If ture, will exit the program after the exception is
                           triggered, exit code is 4. Default false.

        @TryExcept(ValueError)
        def func():
            int('a')
    """


def Retry(
        etype:          'Union[type, Tuple[type, ...]]' = Exception,
        *,
        count:          'int'                           = None,
        cycle:          'Union[int, float]'             = None,
        ignore:         'bool'                          = None,
        output_raw_exc: 'bool'                          = None,
        logger:         'logging.Logger'                = None
) -> 'Callable':
    """
    `Retry` is a decorator, when an exception is raised in function decorated,
    attempt to re-execute the function decorated.

    @param etype:          Which exceptions to try.
    @param count:          The retry count, 0 means infinite, default infinite.
    @param cycle:          The retry cycle, default 0.
    @param ignore:         If true, exception are processed silently without
                           output, default false.
    @param output_raw_exc: If true, output the raw exception information
                           directly,
                           default false. Note priority lower than
                           parameter `ignore`.
    @param logger:         By default, exception information is output to
                           terminal by `sys.stderr`. You can specify this
                           parameter, if you want to output exception
                           information using your logger, it will call the
                           logger's `warning ` method.

        @Retry(count=3, cycle=1)
        def func():
            int('a')

        @TryExcept(ValueError)
        @Retry(count=3, cycle=1)
        def func():
            int('a')
    """


async def TryExceptAsync(
        etype:          'Union[type, Tuple[type, ...]]',
        *,
        ignore:         'bool'                                      = None,
        output_raw_exc: 'bool'                                      = None,
        logger:         'logging.Logger'                            = None,
        ereturn:        'Any'                                       = None,
        ecallback:      'Callable[[Exception, Callable, ...], Any]' = None,
        eexit:          'bool'                                      = None
) -> 'Callable':
    """
    `TryExceptAsync` is a decorator, handle exception raised in asynchronous
    function decorated.

    @param etype:          Which exceptions to handle.
    @param ignore:         If true, exception are processed silently without
                           output, default false.
    @param output_raw_exc: If true, output the raw exception information
                           directly, default false. Note priority lower than
                           parameter `ignore`.
    @param logger:         By default, exception information is output to
                           terminal by `sys.stderr`. You can specify this
                           parameter, if you want to output exception
                           information using your logger, it will call the
                           logger's `error` method.
    @param ereturn:        If not None, it is returned after an exception is
                           raised.
    @param ecallback:      Receives a callable object and called it after an
                           exception is raised. The callable object receive
                           multiple parameters, raised exception object,
                           function decorated and its arguments.
    @param eexit:          If ture, will exit the program after the exception is
                           triggered, exit code is 4. Default false.

        @TryExceptAsync(ValueError)
        async def func():
            int('a')
    """


async def RetryAsync(
        etype:          'Union[type, Tuple[type, ...]]' = Exception,
        *,
        count:          'int'                           = None,
        cycle:          'Union[int, float]'             = None,
        ignore:         'bool'                          = None,
        output_raw_exc: 'bool'                          = None,
        logger:         'logging.Logger'                = None
) -> 'Callable':
    """
    `RetryAsync` is a decorator, when an exception is raised in asynchronous
    function decorated, attempt to re-execute the asynchronous function
    decorated.

    @param etype:          Which exceptions to try.
    @param count:          The retry count, 0 means infinite, default infinite.
    @param cycle:          The retry cycle, default 0.
    @param ignore:         If true, exception are processed silently without
                           output, default false.
    @param output_raw_exc: If true, output the raw exception information
                           directly, default false. Note priority lower than
                           parameter `ignore`.
    @param logger:         By default, exception information is output to
                           terminal by `sys.stderr`. You can specify this
                           parameter, if you want to output exception
                           information using your logger, it will call the
                           logger's `warning ` method.

        @RetryAsync(count=3, cycle=1)
        async def func():
            int('a')

        @TryExceptAsync(ValueError)
        @RetryAsync(count=3, cycle=1)
        async def func():
            int('a')
    """


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    """  QYYYQLLYYYYYYYQLYYQYYQQQYQQYQQQQQQQQQQQQQQQQQQQQQQYYYQQQQQQYL
        YYYYQYLLQYLLYYQYYYYYYYQQYQYQYQQQQQQQQQQQQQQQQQQQQQQQYYYQQQQQQ
        QYYYYLPQYLPLYYYLLYYYYYYYYQQQYQQQQQQQQQQQQQQQQQQQQQQQYYYYQQQQQP
        QYYQLPLQYLLYYQPLLLYYYYYYQYYQYQQQQQQQQQQQQQQYQQQQQQQQYYQYQQQQQQP
       QYYQYLLYYYLLYQYLLYYYYYYYYQYYQYQYYYQQQQQQQQQQYQQQQQQYQQYQYYQQQQQYP
      LQYQYYYYQYYYYYQYYYYYYYYYYYYYYYQQYYYYYYYYYQQQQYQQQQQQYQQYQYYQQQQQQ P
      QYQQYYYYQYYYQQQYYYYYYYYQYQYYYYQQYYYQYQYYQQQQYQQQQQQQYQQYQYYQQQQQQ P
      QYQQYYYYQYYYQQQYYYYYYYYQYQYYYYYQYYYYQYYYQQQQYQQQQQQQYQQYQQYQQQQYYP
      QYQYYYYYQYYYQQQ PYLLLYP PLYYYYYYQYYYYYYQQQQYYQQQQQQYQQYQQQYQQQQYQ
      PQQYYYYYQYYQQYQQQQQQQQQQYP        PPLYQYQYQYQLQQQQQYQQYQQQYYQQQYY
       QQYYYYYQQYQLYQQPQQQQQL QYL           PPYYLYYLQYQQYYQYQQQQYYQPQYL
       YQYYYYQQQYQ  LYLQQQQQQYQQ           YQQQQQGQQQQQQYQYYQQQQYQPQYQ P
      L QYYYYQQLYQ   Y YPYQQQQQ           LQQQQQL YQQQQYQQYQYQQYYQQYQP P
        YYQYYQQ  Q    LQQQQQQY            YQYQQQQQQYYQYLQYQQYQQYYQYQL P
     Y  LYQLQQPL Y     P  P                QLLQQQQQ Q  PQQQQYQQYYQQL P
    P   PYQYQQQQPQ                         PQQQQQQY    QQYQYYQQYYQPP
    L    QQQYQ YYYY              PQ           L  P    LPQYQYYQQLQ P
    Y   PPQQYYL LYQL                                 PQLQYQQYQYQ  L
    Y     QQYQPP PYQY        PQ                      Q  QQYQYQYL  L
    Y     QQYYQ L  QYQP         PLLLLLYL           LQQ LQYYQQQP P L
     L   PPLQYYQ Y  LQQQ                         LQYQ  QYYYQQ     P
      L    Q  QYQ  Y  QQPYL                   PQYYYYPPQYYQQQP    L
       L    L  PQQL   LYQ  PQP             QL PYYYPLQLYQ  QY P   Y
         P   P    PQQP  QY  QLLQQP   LYYLQ   PQYPQQQP P  QY P   L
                       PYQYYY           PQ  PQ      L   Q P    L
              PQYLYYYPQ PLPL             L QY YQYYQYLYQQQ    P
            PYLLLLLYYYQ P  L    P         PYL  PQYYLLLLLLLQ
           LYPLLLLLLYYYY   Y  YQY     LLLPPY   LYYYLLLLLLLLY
           YLLLYLLLLLLYYQ  Q              PQ  YYYLLLLLLLLLLYP
          YLLLLLLLLLLLLLLYQQ              PYYQYYLLLLLLLLYYYLQ
          QLLLLLLLLLLLLLLLLLYYQYP        YQYYLLLLLLLLLLLLLLLQ
          YLLLLLLLLLLLLLLLLLLLYYYLLYYYLLLLLLLLLLLLLLLLLLLLLLYP
         PLLLLLLLLLLLLLLLLLLLLLLLYLLLLLLLLLLLLLLLLLLLLLLLYLYLL
         LLLLLLLLLLYYLLLLLLYLLLLLLLLLLLLLLLL GQYLPY LLLYLYLLLY
         QLLLLYYLYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYYYLLQ
         QLLLLLYYQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQLYYLLLQ
        LYLLYLLLQYYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLQYYYYYLYQ
        YLLLYYLLYQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLYYYYQLLLLY
        QLLLYYYYYQLLLLLLLLLLLLLLYLLLLLLLLLLLLLLLLLLLLYYYLQLLPLLQ
        YLYLLQYYYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYLLLLLYYQYYLLLLLQ
       LYLLLLLYYYQLLYLLLLLLLLLLLLYLYLLYYLLLLYLLLLLLLYYYQQLLLLLLLY
       YLLLLLLYYYQLLYLLLLLLLYLYLLLLLLLLLLLLLLLLLLLLYYYYQQLYLLLLLQ
       QLLLYLLLQYQLQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYYQYYLLLLLLLY
       QLLLLLLLLQQYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYQYYLLLLLLLQ
       QLLLLLLLLLQQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYYYLLLLLLLLLYL
       QLLLLYLYYLYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYYLLLLLLLLLQ
       YLLLLLLLYYLQLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLLLLYQYYLLLLLLLLLQ
       QLLLLLYLYYYYLLLLLPLLLLLLLYLYLLLLLLLLLLLLLLLLLLLQYYLLLLLLLLYP
       YYLYYLLYYYQLLLLLLLLYLLLLLLLLLLLLLLLLLLLLLLYLYLLYQYYLLLLLLYL
        QLLLLLLYQYLLLLLLLLLLLLLLLLLLLLLYYLYLLLLLLLLLLLYQQQQQQQLYL  """
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']
    ge = gcode.GqylpyException()

    for gname, gvalue in globals().items():
        if gname[0] != '_' and hasattr(gcode, gname):
            gfunc = getattr(gcode, gname)
            gfunc.__module__ = __package__
            setattr(ge, gname, gfunc)
        if gname[:2] == '__' and gname != '__builtins__':
            setattr(ge, gname, gvalue)

    ge.__module__ = __package__
    sys.modules[__name__] = ge.GqylpyException = ge


import logging
from typing import Union, Tuple, Callable, Any
