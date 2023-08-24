print('<[100]> evalsupport module start')

def deco_alpha(cls):
    print('<[200]> deco_alpha')

    def inner_1(self):
        print('<[300]> deco_alpha:inner_1')

    cls.method_y = inner_1
    return cls


class MetaAleph(type):  # 元类
    print('<[400]> MetaAleph body')

    def __init__(cls, name, bases, dic): # cls，表明要构建的对象是类
        print('<[500]> MetaAleph.__init__')

        def inner_2(self):  # self，最终要构建的类对象
            print('<[600]> MetaAleph.__init__:inner_2')

        cls.method_z = inner_2


print('<[700]> evalsupport module end')