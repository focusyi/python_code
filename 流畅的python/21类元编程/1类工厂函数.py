'''
类工厂函数
缺点：不能序列化
'''
# BEGIN RECORD_FACTORY
def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()  # <1> 鸭子类型，拆成可迭代对象
    except AttributeError:  # no .replace or .split
        pass  # assume it's already a sequence of identifiers
    field_names = tuple(field_names)  # <2> 使用属性名构建元组

    def __init__(self, *args, **kwargs):  # <3> 
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):  # <4>  把对象变成可迭代对象，按照__slot__设定的顺序产出值
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):  # <5>
        values = ', '.join('{}={!r}'.format(*i) for i
                           in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__ = field_names,  # <6>
                     __init__  = __init__,
                     __iter__  = __iter__,
                     __repr__  = __repr__)

    return type(cls_name, (object,), cls_attrs)  # <7>调用type构造方法构建新类，type 是一个类。当成类使用时，传入三个参数可以新建一个类
# END RECORD_FACTORY

Dog = record_factory('Dog', 'name, weight, owner')
rex = Dog(name='Rex', weight=20, owner='Bob')
print(rex)

name, weight, _ = rex # 可迭代对象，可以顺利拆包
print(name, weight)

rex.weight = 32     # 可变对象
print(rex)

print(Dog.__mro__)  # 继承自object,与工厂函数无关