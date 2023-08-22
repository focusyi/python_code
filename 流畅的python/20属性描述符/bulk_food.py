"""

A line item for a bulk food order has description, weight and price fields::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)

A ``subtotal`` method gives the total price for that line item::

    >>> raisins.subtotal()
    69.5

The weight of a ``LineItem`` must be greater than 0::

    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0

Negative or 0 price is not acceptable either::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0


No change was made::

    >>> raisins.weight
    10

"""


# BEGIN LINEITEM_V3
class Quantity:  # <1> 描述符类，基于协议实现

    def __init__(self, storage_name):
        self.storage_name = storage_name  # <2>

    def __set__(self, instance, value):  # <3>为托管属性赋值。instance托管实例，value要设定的值
        if value > 0:
            instance.__dict__[self.storage_name] = value  # <4> 必须适用__dict__ 属性；如果使用内置的setattr 函数，会再次触发 __set__ 方法，导致无限递归
        else:
            raise ValueError('value must be > 0')


class LineItem:
    # 缺点：在托管类的定义体中实例化描述符时要重复输入两次属性的名称，比如：weight
    # 由于赋值语句是等号右边先执行，会造成创建完实例后，赋值给错误的变量，造成程序错误
    weight = Quantity('weight')  # <5>
    price = Quantity('price')  # <6>

    def __init__(self, description, weight, price):  # <7>
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# END LINEITEM_V3


# 版本二：创建描述符实例时不需要创建名称，可以在创建对象时生成唯一名字
class Quantity:
    __counter = 0  # <1>

    def __init__(self):
        cls = self.__class__  # <2>Quantity类的引用
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)  # <3> 每个对象的storage_name都是唯一的
        cls.__counter += 1  # <4>

    def __get__(self, instance, owner):  # <5> owner是托管类（如 LineItem）的引用，通过描述符从托管类中获取属性时用得到
        return getattr(instance, self.storage_name)  # <6> 获取属性值
    # def __get__(self, instance, owner):
    #     if instance is None:
    #         return self  # <1> 为了给用户提供内省和其他元编程技术支持，通过类访问托管属性时，最好让 __get__ 方法返回描述符实例
    #     else:
    #         return getattr(instance, self.storage_name)  # <2>

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)  # <7> 把值存储在instance中
        else:
            raise ValueError('value must be > 0')
    # 这里可以使用内置的高阶函数 getattr 和 setattr 存取值，无需使用instance.__dict__，因为托管属性和储存属性的名称不同，所以把
    # 储存属性传给 getattr 函数不会触发描述符，不会无限递归


class LineItem:
    weight = Quantity()  # <8>
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price