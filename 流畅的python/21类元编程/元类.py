'''
比较执行顺序
导入时：python窗口 import 元类； 执行顺序：顶层导入-->类定义体-->执行时函数体-->父类初始化
运行时：cmd窗口 python 元类.py
'''
from evalsupport import deco_alpha
from evalsupport import MetaAleph

print('<[1]> evaltime_meta module start')


@deco_alpha
class ClassThree():
    print('<[2]> ClassThree body')

    def method_y(self):
        print('<[3]> ClassThree.method_y')


class ClassFour(ClassThree):
    print('<[4]> ClassFour body')

    def method_y(self):
        print('<[5]> ClassFour.method_y')


class ClassFive(metaclass=MetaAleph):
    print('<[6]> ClassFive body')   # 创建 ClassFive 时调用了MetaAleph.__init__ 方法。

    def __init__(self):
        print('<[7]> ClassFive.__init__')

    def method_z(self):
        print('<[8]> ClassFive.method_y')


class ClassSix(ClassFive):
    print('<[9]> ClassSix body') #创建 ClassFive 的子类 ClassSix 时也调用了MetaAleph.__init__ 方法。

    def method_z(self):
        print('<[10]> ClassSix.method_y')


if __name__ == '__main__':
    print('<[11]> ClassThree tests', 30 * '.')
    three = ClassThree()
    three.method_y()    # 因为有装饰器，method_y方法被替换成inner_1 方法
    print('<[12]> ClassFour tests', 30 * '.')
    four = ClassFour()
    four.method_y()     # 子类没有受装饰器影响
    print('<[13]> ClassFive tests', 30 * '.')
    five = ClassFive()
    five.method_z()     # MetaAleph 类的 __init__ 方法把 ClassFive.method_z 方法替换成 inner_2 函数
    print('<[14]> ClassSix tests', 30 * '.')
    six = ClassSix()      # ClassFive 的子类 ClassSix 也是一样，method_z 方法被替换成 inner_2 函数
    six.method_z()

print('<[15]> evaltime_meta module end')