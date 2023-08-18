"""

"""

# BEGIN SENTENCE_ITER
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):  # <1> 该类可以迭代
        return SentenceIterator(self.words)  # <2> 返回一个迭代器
    
    def __iter__(self):
        for word in self.words:  # <1> # 
            yield word  # <2> 生成器函数代替SentenceIterator 类
        return  # <3> 可以省略return


class SentenceIterator:

    def __init__(self, words):
        self.words = words  # <3>
        self.index = 0  # <4>

    def __next__(self):
        try:
            word = self.words[self.index]  # <5>
        except IndexError:
            raise StopIteration()  # <6>
        self.index += 1  # <7>
        return word  # <8>

    def __iter__(self):  # <9>
        return self
# END SENTENCE_ITER



# 第二版生成器，懒惰求值
class Sentence:

    def __init__(self, text):
        self.text = text  # <1>

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):  # <2> 返回一个迭代器，不用提前把文本找到放到内存中
            yield match.group()  # <3>

# 第三版，生成器表达式
class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        # 使用生成器表达式构建生成器，然后将其返回，最后iter方法还是返回一个生成器对象
        return (match.group() for match in RE_WORD.finditer(self.text))


def main():
    import sys
    import warnings
    try:
        filename = sys.argv[1]
        word_number = int(sys.argv[2])
    except (IndexError, ValueError):
        print('Usage: %s <file-name> <word-number>' % sys.argv[0])
        sys.exit(1)
    with open(filename, 'rt', encoding='utf-8') as text_file:
        s = Sentence(text_file.read())
    for n, word in enumerate(s, 1):
        if n == word_number:
            print(word)
            break
    else:
        warnings.warn('last word is #%d, "%s"' % (n, word))

if __name__ == '__main__':
    main()