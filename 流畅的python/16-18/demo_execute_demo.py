# BEGIN EXECUTOR_MAP
from time import sleep, strftime
from concurrent import futures


def display(*args):  # <1>
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):  # <2>
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10  # <3>


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  # <4>
    # executor.map, 只能处理同一个可等待对象是什么意思？？
    results = executor.map(loiter, range(5))  # <5>3个线程执行5个io操作
    display('results:', results)  # <6>.
    display('Waiting for individual results:')
    for i, result in enumerate(results):  # <7> 这一步获取结果是阻塞的，需要future对象执行完毕才能获取结果
        display('result {}: {}'.format(i, result))


main()