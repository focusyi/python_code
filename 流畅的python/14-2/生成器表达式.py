def gen_AB(): # 
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')

res1 = [x*3 for x in gen_AB()]  # 列表推导式，会提前执行生成器函数中的代码
res2 = (x*3 for x in gen_AB()) # 生成器表达式，会在后面for循环中再执行代码，占用更少内存
print(type(res1), type(res2))