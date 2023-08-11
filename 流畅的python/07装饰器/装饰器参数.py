'''
装饰器接收参数
'''

'''
registry = set()  # <1>

def register(active=True):  # <2>
    def decorate(func):  # <3> 装饰器工厂函数，参数是被装饰的函数，用来处理参数
        print('running register(active=%s)->decorate(%s)'
              % (active, func))
        if active:   # <4> 如果active为True，才把func添加到registry中
            registry.add(func)
        else:
            registry.discard(func)  # <5>

        return func  # <6>
    return decorate  # <7>

@register(active=False)  # <8>
def f1(a, b):
    print(a + b)
    print('running f1()')

@register()  # <9>
def f2():
    print('running f2()')

def f3():
    print('running f3()')

print(f1(3, 4))
'''


# 示例二

import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):  # <1>
    def decorate(func):      # <2> 真正的装饰器
        def clocked(*_args): # <3> 被包装的函数
            t0 = time.time()
            _result = func(*_args)  # <4> 被装饰函数真正的返回结果
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)  # <5>
            result = repr(_result)  # <6>
            print(fmt.format(**locals()))  # <7>
            return _result  # <8>
        return clocked  # <9>
    return decorate  # <10>

if __name__ == '__main__':

    @clock()  # <11>
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)
