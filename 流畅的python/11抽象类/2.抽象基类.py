# 抽象基类的本质就是几个特殊方法
class Struggle:
    def __len__(self): return 23
from collections import abc
# abc.Sized 也能把 Struggle 识别为自己的子类，只要实现了特殊方法 __len__ 即可
print(isinstance(Struggle(), abc.Sized))

# 如果必须强制执行 API 契约，通常可以使用 isinstance 检查抽象基类这对采用插入式架构的系统来说特别有用

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

# collections.MutableSequence抽象基类，用于表示可变序列类型，定义了一些必须实现的方法
class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):  # <1>抽象方法
        self._cards[position] = value

    def __delitem__(self, position):  # <2> 这是一个抽象方法，必须实现
        del self._cards[position]

    def insert(self, position, value):  # <3> 这也是一个抽象方法
        self._cards.insert(position, value)
# 导入时（加载并编译 frenchdeck2.py 模块时），Python 不会检查抽象方
# 法的实现，在运行时实例化 FrenchDeck2 类时才会真正检查。
F = FrenchDeck2()

