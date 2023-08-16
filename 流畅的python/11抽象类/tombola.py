import abc

class Tombola(abc.ABC):  # <1>自定义抽象类要继承abc.ABC

    @abc.abstractmethod
    def load(self, iterable):  # <2>abstractmethod装饰器定义抽象方法
        """Add items from an iterable."""

    @abc.abstractmethod
    def pick(self):  # <3>
        """随机删除元素并返回.

        This method should raise `LookupError` when the instance is empty.
        """

    def loaded(self):  # <4>
        """Return `True` if there's at least 1 item, `False` otherwise."""
        return bool(self.inspect())  # <5> 抽象基类中的具体方法只能依赖抽象基类定义的接口


    def inspect(self):
        """Return a sorted tuple with the items currently inside."""
        items = []
        while True:  # <6>
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # <7>
        return tuple(sorted(items))
# 抽象方法可以有实现代码。即便实现了，子类也必须
# 覆盖抽象方法，但是在子类中可以使用 super() 函数调用抽象方
# 法，为它添加功能，而不是从头开始实现

