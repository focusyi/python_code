class Foo:
    def __init__(self) -> None:
        self.card = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __len__(self):
        return len(self.card)

    def __getitem__(self, pos):
        return self.card[pos]
    
    # def __setitem__(self, pos, value):
    #     self.card[pos] = value
# Foo 实例是可迭代的对象，因为发现有__getitem__ 方法时，Python 会调用它
# 鉴于序列协议的重要性，如果没有 __iter__ 和 __contains__方法，Python 会调用 __getitem__ 方法，设法让迭代和 in 运算符可用。
# Python 中的迭代是鸭子类型的一种极端形式：为了迭代对象，解释器会尝试调用两个不同的方法
f = Foo()
print(f[1])

for i in f:
    print(i)
print(20 in f)
print(len(f))

# 打乱顺序需要对序列修改，因此要实现__setitem__方法
from random import shuffle
# print(shuffle(f), f.card)

# 猴子补丁，为了在运行时实现协议，而不用修改源码，这就是猴子补丁
# 加入Foo类没有实现__setitem__方法，可以在运行时动态修改
def set_card(f, pos, value):
    f.card[pos] = value
print(hasattr(f, '__setitem__'))
# 给类添加方法
Foo.__setitem__ = set_card
print(hasattr(f, '__setitem__'))
print(shuffle(f), f.card)

# “鸭子类型”：对象的类型无关紧要，只要实现了特定的协议即可，所以有的时候，
# 鸭子类型：只要会呱呱叫的都是鸭子
# isinstance：必须继承自鸭子类，认鸭作父

# 白鹅类型（goose typing）。
# 白鹅类型指，只要 cls 是抽象基类，即 cls 的元类是abc.ABCMeta，就可以使用 isinstance(obj, cls)

# Python 的抽象基类还有一个重要的实用优势：可以使用 register
# 类方法在终端用户的代码中把某个类“声明”为一个抽象基类的“虚
# 拟”子类（为此，被注册的类必须满足抽象基类对方法名称和签名
# 的要求，最重要的是要满足底层语义契约；但是，开发那个类时不
# 用了解抽象基类，更不用继承抽象基类）。这大大地打破了严格的
# 强耦合，与面向对象编程人员掌握的知识有很大出入，因此使用继
# 承时要小心。

