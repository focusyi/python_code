#!/usr/bin/env python3

# spinner_asyncio.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_ASYNCIO
import asyncio
import itertools
import sys


@asyncio.coroutine  # <1> 该装饰器在3.8中已经被废弃
def spin(msg):  # <2>
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)  # <3>
        except asyncio.CancelledError:  # <4> 捕获cancel异常，退出协程
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():  # <5>
    # pretend waiting a long time for I/O
    yield from asyncio.sleep(3)  # <6> 休眠3s，模拟io操作，把控制权交给主循环，主循环继续运行，执行其他协程
    return 42


@asyncio.coroutine
def supervisor():  # <7>
    spinner = asyncio.ensure_future(spin('thinking!'))  # <8> 创建一个task对象，用于执行spin协程，这里创建的task已经被注册到事件循环中，会自动执行
    print('spinner object:', spinner)  # <9>
    result = yield from slow_function()  # <10> 执行slow_function
    spinner.cancel()  # <11> 取消spin协程，协程可以取消，线程不能取消，因为线程会随时被系统中断。协程向比较线程，不需要锁，因为就一个线程在执行，而且线程人工进行中断，不存在数据安全问题
    return result


def main():
    loop = asyncio.get_event_loop()  # <12>
    result = loop.run_until_complete(supervisor())  # <13>
    loop.close()
    print('Answer:', result)



if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO