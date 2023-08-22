'''
描述符和方法的运作方式
'''
# BEGIN FUNC_DESCRIPTOR_EX
import collections


class Text(collections.UserString):

    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]

# END FUNC_DESCRIPTOR_EX
word = Text('forward')
print(word, word.reverse())
print(Text.reverse(Text('backword'))) # 在类上调用方法相当于调用函数
# 方法当函数使用
print(list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')])))

print(Text.reverse.__get__(word)) # 函数是非覆盖描述符，调用__get__方法，得到对象的绑定方法
print(Text.reverse.__get__(None, word)) # 如果 instance 参数的值是 None，那么得到的是函数本身

print(word.reverse) # 调用的是Text.reverse.__get__(word)返回的绑定方法
print(word.reverse.__self__) # 绑定方法的__self__属性，就是对象的引用
print(word.reverse.__func__ is Text.reverse) # 绑定方法的__func__属性就是类上的原始函数的引用
