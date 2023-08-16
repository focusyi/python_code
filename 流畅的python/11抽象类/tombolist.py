from random import randrange

from tombola import Tombola

@Tombola.register  # <1> 注册为 Tombola 的虚拟子类
class TomboList(list):  # <2> 继承 list

    def pick(self):
        if self:  # <3>
            position = randrange(len(self))
            return self.pop(position)  # <4>
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend  # <5>

    def loaded(self):
        return bool(self)  # <6>

    def inspect(self):
        return tuple(sorted(self))

print(TomboList.__mro__)