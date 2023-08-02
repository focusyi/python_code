import asyncio

async def my_coroutine():
    print("Coroutine is running...")

async def main():
    # task = asyncio.create_task(my_coroutine())
    asyncio.create_task(my_coroutine())
    # await task # task创建时已经排定好执行时机了，不需要手动调用await，除非想要获取返回值

asyncio.run(main())