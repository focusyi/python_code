b = '盖伦'
def func1(a):
    '''
    读取一个局部变量和一个全局变量
    '''
    print(a)
    print(b)
    
func1('瑞文')

def func2(a):
    '''
    读取两个局部变量
    Python 不要求声明变量，但是假定在函数定义体中赋值的变量是局部变量。所以 打印b会报错
    '''
    print(a)
    print(b)
    b = '亚索'
    
# func2('瑞文')

def func3(a):
    '''
    读取一个局部变量和一个全局变量，可以查看字节码查看区别dis.dis(func3)
    dis文档：http://docs.python.org/3/library/dis.html
    '''
    global b
    print(a)
    print(b)
    b = '亚索'
    
func3('瑞文')