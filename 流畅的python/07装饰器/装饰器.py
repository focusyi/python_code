import time
import functools

# 定义一个装饰器，用来计算函数的运行时间
def clock(func):
    # functools.wraps 装饰器把相关的属性从 func 复制到 clocked 中。此外，新版还能正确处理关键字参数
    @functools.wraps(func)
    def clocked(*args):
        t0 = time.time()
        result = func(*args)
        elapsed = time.time() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

# 装饰器等价于
# factorial = clock(factorial)

print(factorial(10)) # 0.00050330s
print(factorial.__name__)  # clocked, factorial是clocked的引用


# 第二版
@clock
def factorial(n):
    # return 1 if n < 2 else n*factorial(n-1)
    return 1 if n < 2 else factorial(n-2) + factorial(n-1)
print(factorial(10)) # 0.03929520s

@functools.lru_cache() # lru_cache() 装饰器把耗时的函数的结果保存起来，避免传入相同的参数时重复计算
@clock
def factorial(n):
    # return 1 if n < 2 else n*factorial(n-1)
    return 1 if n < 2 else factorial(n-2) + factorial(n-1)
print(factorial(10)) # 0.00625491s

class MyClass:
    def __init__(self, x):
        self.x = x

    def foo(self, a, b):
        return a + b

    def bar(self, a, b):
        return a * b

obj = MyClass(42)
print(dir(obj))
import inspect
print(inspect.getmembers(obj, inspect.ismethod)) # 获取对象的方法列表
method_list = [method for method in inspect.getmembers(obj, inspect.ismethod) if not method[0].startswith('__')]
print(method_list) # 获取对象的方法列表
for method in method_list:
    print(method[0], method[1](2, 3))