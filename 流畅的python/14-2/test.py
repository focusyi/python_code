# import abc
from collections import abc
# 普通类
# class Foo:
#     pass

# f = Foo()
# for i in f: # TypeError: 'Foo' object is not iterable
#     print(i)


class Foo2:
    def __iter__(self): # 返回一个迭代器
        print(111)
        return self
f = Foo2()
print(issubclass(Foo2, abc.Iterable)) # True
print(isinstance(f, abc.Iterable))      # True
print(iter(f)) # 检查对象 x 能否迭代，最准确的方法
for i in f: # TypeError: 'Foo' object is not iterable
    print(i)