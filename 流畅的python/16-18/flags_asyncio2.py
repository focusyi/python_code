import asyncio
import collections
import contextlib

import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):  # <1>
    def __init__(self, country_code):
        self.country_code = country_code


@asyncio.coroutine
def get_flag(base_url, cc): # <2>
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    with contextlib.closing(resp):
        if resp.status == 200:
            image = yield from resp.read()
            return image
        elif resp.status == 404:
            raise web.HTTPNotFound()
        else:
            raise aiohttp.HttpProcessingError(
                code=resp.status, message=resp.reason,
                headers=resp.headers)


@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):  # <3>asyncio.semaphore用于限制并发请求数量
    try:
        with (yield from semaphore):  # <4> 在 yield from 表达式中把 semaphore 当成上下文管理器使用，防止阻塞整个系统：如果 semaphore 计数器=0，在这里阻塞
            image = yield from get_flag(base_url, cc)  # <5>退出with 语句后，semaphore 计数器的值会递减
    except web.HTTPNotFound:  # <6>
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc  # <7>
    else:
        save_flag(image, cc.lower() + '.gif')  # <8>
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)
# END FLAGS2_ASYNCIO_TOP

# BEGIN FLAGS2_ASYNCIO_DOWNLOAD_MANY
@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, concur_req):  # <1>
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)  # <2> semaphore内部维护一个计数器，它的 acquire() 计数器+1和 release() 计数器-1方法会在协程访问共享资源时被调用。
    to_do = [download_one(cc, base_url, semaphore, verbose)
             for cc in sorted(cc_list)]  # <3>

    to_do_iter = asyncio.as_completed(to_do)  # <4> as_completed() 函数的参数是一个 Future 实例列表，返回值是一个迭代器，在期物运行结束后产出期物。
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # <5>
    for future in to_do_iter:  # <6>
        try:
            res = yield from future  # <7> 从期物中获取结果，代替 yield future.result()
        except FetchError as exc:  # <8>
            country_code = exc.country_code  # <9>
            try:
                error_msg = exc.__cause__.args[0]  # <10>
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__  # <11>
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status

        counter[status] += 1  # <12>

    return counter  # <13>


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)  # <14>
    loop.close()  # <15>

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)