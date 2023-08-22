"""
Overriding descriptor (a.k.a. data descriptor or enforced descriptor):

# BEGIN DESCR_KINDS_DEMO1

    >>> obj = Managed()  # <1>
    >>> obj.over  # <2>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> Managed.over  # <3>
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    >>> obj.over = 7  # <4>
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
    >>> obj.over  # <5>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> obj.__dict__['over'] = 8  # <6>
    >>> vars(obj)  # <7>
    {'over': 8}
    >>> obj.over  # <8>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

# END DESCR_KINDS_DEMO1

Overriding descriptor without ``__get__``:

(these tests are reproduced below without +ELLIPSIS directives for inclusion in the book;
look for DESCR_KINDS_DEMO2)

    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> Managed.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.__dict__['over_no_get'] = 9
    >>> obj.over_no_get
    9
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get
    9

Non-overriding descriptor (a.k.a. non-data descriptor or shadowable descriptor):

# BEGIN DESCR_KINDS_DEMO3

    >>> obj = Managed()
    >>> obj.non_over  # <1>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    >>> obj.non_over = 7  # <2>
    >>> obj.non_over  # <3>
    7
    >>> Managed.non_over  # <4>
    -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
    >>> del obj.non_over  # <5>
    >>> obj.non_over  # <6>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)

# END DESCR_KINDS_DEMO3

No descriptor type survives being overwritten on the class itself:

# BEGIN DESCR_KINDS_DEMO4

    >>> obj = Managed()  # <1>
    >>> Managed.over = 1  # <2>
    >>> Managed.over_no_get = 2
    >>> Managed.non_over = 3
    >>> obj.over, obj.over_no_get, obj.non_over  # <3>
    (1, 2, 3)

# END DESCR_KINDS_DEMO4

Methods are non-overriding descriptors:

    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> Managed.spam  # doctest: +ELLIPSIS
    <function Managed.spam at 0x...>
    >>> obj.spam()
    -> Managed.spam(<Managed object>)
    >>> Managed.spam()
    Traceback (most recent call last):
      ...
    TypeError: spam() missing 1 required positional argument: 'self'
    >>> Managed.spam(obj)
    -> Managed.spam(<Managed object>)
    >>> Managed.spam.__get__(obj)  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> obj.spam.__func__ is Managed.spam
    True
    >>> obj.spam = 7
    >>> obj.spam
    7


"""

"""
NOTE: These tests are here because I can't add callouts after +ELLIPSIS
directives and if doctest runs them without +ELLIPSIS I get test failures.

# BEGIN DESCR_KINDS_DEMO2

    >>> obj.over_no_get  # <1>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> Managed.over_no_get  # <2>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> obj.over_no_get = 7  # <3>
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # <4>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> obj.__dict__['over_no_get'] = 9  # <5>
    >>> obj.over_no_get  # <6>
    9
    >>> obj.over_no_get = 7  # <7>
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # <8>
    9

# END DESCR_KINDS_DEMO2

Methods are non-overriding descriptors:

# BEGIN DESCR_KINDS_DEMO5

    >>> obj = Managed()
    >>> obj.spam  # <1>
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x74c80c>>
    >>> Managed.spam  # <2>
    <function Managed.spam at 0x734734>
    >>> obj.spam = 7  # <3>
    >>> obj.spam
    7

# END DESCR_KINDS_DEMO5

"""

# BEGIN DESCR_KINDS

### auxiliary functions for display only ###

def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls 
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))

def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


### essential classes for this example ###

class Overriding:  # <1> 定义了get和set，属于覆盖型描述符
    """a.k.a. data descriptor or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # <2>

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # <3> 没有定义get的覆盖型描述符
    """an overriding descriptor without ``__get__``"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # <4>    没有定义set的非覆盖型描述符
    """a.k.a. non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:  # <5> 托管类，使用描述符对象
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # <6>
        print('-> Managed.spam({})'.format(display(self)))

# END DESCR_KINDS
## 测试覆盖型描述符行为
'''
obj = Managed()
print(obj.over, Managed.over) # 触发描述符的get方法，读取描述符的值
obj.over = 777 # 触发描述符的set方法
print(obj.over)     # 触发描述符的get方法
obj.__dict__['over'] = 888  # 跳过描述符，添加属性
print(vars(obj))
print(obj.over)     # 触发描述符的get方法,覆盖对象的over属性
'''
## 测试没有get的覆盖型描述符行为
'''
obj = Managed()
print(obj.over_no_get, Managed.over_no_get)  # 从类中获取描述符实例？？？这是啥意思
obj.over_no_get = 777   # 触发__set__方法

obj.__dict__['over_no_get'] = 999
obj.over_no_get = 777   # 触发__set__方法

print(obj.over_no_get)      # 999,对象的over_no_get属性覆盖描述符，只有读操作是这样
'''

## 测试非覆盖型描述符
'''
obj = Managed()
print(obj.non_over) # 触发描述符的__get__方法
obj.non_over = 777  # 由于没有__set__方法，所以不干涉对象属性赋值
print(obj.non_over)     # 对象属性把描述符覆盖掉
print(Managed.non_over)     # 触发描述符的__get__方法
del obj.non_over    # 删除对象属性，就会恢复读取__get__方法描述符
print(obj.non_over)
'''

## 在类中覆盖描述符
'''
obj = Managed()
Managed.over = 111 # 覆盖类中的描述符
Managed.over_no_get = 222
Managed.non_over = 333
print(obj.over, obj.over_no_get, obj.non_over) # 没有调用描述符的__get__方法
'''

## 方法是非覆盖型描述符
obj = Managed()
print(obj.spam) # 获取的是绑定方法对象
print(Managed.spam) # 函数
obj.spam = 777 # 覆盖类属性，obj无法访问spam方法，函数都实现了__get__方法，没有实现 __set__ 方法，因此是非覆盖型描述符

