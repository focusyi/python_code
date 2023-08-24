import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value

# BEGIN MODEL_V6
def entity(cls):  # <1> 类装饰器的参数是类
    for key, attr in cls.__dict__.items():  # <2>   迭代类属性
        if isinstance(attr, Validated):  # <3>  如果类属性是描述符Validated的属性
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)  # <4>使用描述符和托管属性的名称命名storage_name
    return cls  # <5>
# END MODEL_V6


@entity  # <1>添加一个类装饰器
class LineItem:
    '''
    类装饰器有个重大缺点：只对直接依附的类有效。这意味着，被装饰的类的子类可能继承也可能不继承装饰器所做的改动，
    具体情况视改动的方式而定
    '''
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

raisins = LineItem('Golden raisins', 10, 6.95)
print(dir(raisins)[:3]) # ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']

print(LineItem.description.storage_name)
print(raisins.description, getattr(raisins, '_NonBlank#description'))