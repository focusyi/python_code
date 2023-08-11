'''
# 版本一：计算平均值，记录历史值
def make_averager(): 
    series = []
    # 闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。
    def averager(new_value):
        series.append(new_value) #series是自由变量(free variable)
        total = sum(series)
        return total/len(series)

    return averager

avg = make_averager()
print(avg(10))
print(avg(20))
print(avg(30))

# 包含了函数定义体中所有的局部变量名
avg.__code__.co_varnames #('new_value', 'total')
# 包含了函数定义体中所有的自由变量名
avg.__code__.co_freevars # ('series',)
# 访问函数对象 avg 的闭包属性，包含了函数对象引用的所有外部变量的值
avg.__closure__  # (<cell at 0x...: list object at 0x...>,)
avg.__closure__[0].cell_contents  # [10, 11, 12]
'''

def make_averager():
    # 记录数据个数和总数
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total # 声明count和total是非局部变量
        count += 1 # 因为赋值操作，count从自由变量变成了局部变量
        total += new_value
        return total / count
    return averager

avg = make_averager()
print(avg(10))
print(avg(20))
print(avg(30))
