import timeit

TIMES = 10000

SETUP = """
symbols = '$¢£¥€¤'
def non_ascii(c):
    return c > 127
"""

def clock(label, cmd):
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES) # 测量代码执行时间 cmd: 要执行的代码，setup: 运行代码的次数，number: 每次运行重复次数
    print(label, *('{:.3f}'.format(x) for x in res))

clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')

# map/filter 组合起来用不一定比列表推导式快

# 列表推导式实现笛卡尔积
[print(x, y) for x in range(3) for y in range(3)]



t = (1, 2, [10, 20])
t[2] += [30, 40]