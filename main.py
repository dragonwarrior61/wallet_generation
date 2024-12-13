import sys
import os
sys.path.append(os.path.abspath("ganache-be"))
from sdk import GanacheSDK
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def generate_wallet_with_prefix(prefix):
    # TODO: - Please optimize time performance of this function. Only modify code in this function.
    start_time = time.time()
    ganache_sdk = GanacheSDK()

    # def task():
    #     wallet = ganache_sdk.generate_wallet()
    #     if wallet[0].startswith(prefix):
    #         return wallet
    #     return None
    # # print(wallet)
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     while(True):
    #         wallet = task()
    #         if wallet is not None:
    #             executor.shutdown(wait=False, cancel_futures=True)
    #             return wallet
    def task():
        wallet = ganache_sdk.generate_wallet()
        # if wallet[0].startswith(prefix):
        #     return wallet
        return wallet

    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
        while(True):
            futures = [executor.submit(task) for _ in range(1000)]
            
            for future in as_completed(futures):  # Process completed tasks as they finish
                wallet = future.result()  # Get the wallet result from the future
                if wallet[0].startswith(prefix):  # Check if the wallet matches the prefix
                    executor.shutdown(wait=False)  # Shutdown the executor
                    return wallet
    raise RuntimeError("No wallet found with the given prefix.")


def main():
    start_time = time.time()
    wallet = generate_wallet_with_prefix('0x1234')
    print(wallet)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


if __name__=='__main__':
    if GanacheSDK().verify_certificate():
        main()
    else:
        print(
            'Error -1: Ganache is not yet installed or configured properly. Please run "python setup_ganache.py" to install it.')