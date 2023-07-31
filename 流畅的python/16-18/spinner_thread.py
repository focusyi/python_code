#!/usr/bin/env python3

# spinner_thread.py

# credits: Adapted from Michele Simionato's
# multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_THREAD
import threading
import itertools
import time
import sys


def spin(msg, done):  # <2>
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # <3>
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # <4>
        if done.wait(.1):  # <5> 如果done被设置，等待0.1s
            break
    write(' ' * len(status) + '\x08' * len(status))  # <6>


def slow_function():  # <7>
    # pretend waiting a long time for I/O
    time.sleep(3)  # <8>
    return 42


def supervisor():  # <9>
    done = threading.Event()        # 创建一个事件对象，用于线程之间的通信，其他线程等待该事件对象被设置时，唤醒线程并继续执行
    spinner = threading.Thread(target=spin,
                               args=('thinking!', done))
    print('spinner object:', spinner)  # <10>   打印线程对象
    spinner.start()  # <11> 启动子线程
    result = slow_function()  # <12>
    done.set()  # <13> 设置信号done,唤醒等待该事件对象的子线程
    spinner.join()  # <14> 等待子线程结束
    return result


def main():
    result = supervisor()  # <15>
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_THREAD