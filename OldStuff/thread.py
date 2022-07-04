from time import sleep
from threading import Thread


def function_1():
    print('function 1 started...')
    while True:
        print('1')
        sleep(1)


def function_2():
    print('function 2 started...')
    while True:
        print('2')
        sleep(1)


thread_1 = Thread(target=function_1)
thread_2 = Thread(target=function_2)
thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
# print("thread finished") - redundant
