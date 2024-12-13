import sys
import os
import time
import asyncio

sys.path.append(os.path.abspath("ganache-be"))
from sdk import GanacheSDK


async def generate_wallet_with_prefix(prefix):
    # Optimized for asynchronous processing
    ganache_sdk = GanacheSDK()

    async def task():
        wallet = ganache_sdk.generate_wallet()
        if wallet[0].startswith(prefix):
            return wallet
        return None

    tasks = [task() for _ in range(10000)]
    for task in asyncio.as_completed(tasks):
        wallet = await task
        if wallet is not None:
            return wallet

    raise RuntimeError("No wallet found with the given prefix.")


async def main():
    start_time = time.time()
    wallet = await generate_wallet_with_prefix('0x1234')
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    print(f"Generated wallet: {wallet}")


if __name__ == '__main__':
    if GanacheSDK().verify_certificate():
        asyncio.run(main())  # Use asyncio.run() to execute the async main
    else:
        print(
            'Error -1: Ganache is not yet installed or configured properly. '
            'Please run "python setup_ganache.py" to install it.'
        )
