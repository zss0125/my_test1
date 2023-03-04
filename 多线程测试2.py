import pandas as pd
import os
import time
import datetime
import warnings
import akshare as ak
import requests

from multiprocessing import Process
from threading import Thread
from MyTT import *

pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('max_colwidth', 100)  # 设置value的显示长度
pd.set_option('display.width', 1000)  # 设置1000列时才换行
warnings.filterwarnings("ignore")  # 抑制警告


# 时间装饰器
def timer():
    def wrapper(func):
        def deco(*args, **kw):
            t1 = time.time()
            func(*args, **kw)
            t2 = time.time()
            cost_time = t2 - t1
            print("花费时间：{}秒".format(cost_time))

        return deco

    return wrapper


# 重写Thread类
class MyThread(Thread):
    """重写多线程，使其能够返回值"""

    def __init__(self, target=None, args=()):
        super(MyThread, self).__init__()
        self.func = target
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def cal_sum(begin, end):
    # global _sum
    _sum = 0
    for i in range(begin, end + 1):
        _sum += i
    return _sum


@timer()
def generate_df(l, w):
    nums = [[i for i in range(l)] for _ in range(w)]
    colu = [f'col_{i}' for i in range(l)]  # 用来做列名
    inde = [f'row_{i}' for i in range(w)]  # 用来做索引
    df = pd.DataFrame(data=nums, index=inde, columns=colu)
    return df



def generate_df1():
    stock_df = ak.stock_zh_a_hist('601318', 'daily', '20220101', '20221231')



# df = generate_df1('601001')

# code_list = ['601001', '601318', '603337', '300642', '300685', '300418', '002585', '002833']
# for security_code in code_list:  # 逐个获取每支证券的df

if __name__ == '__main__':
# df = generate_df(3, 5)
# print(df)
#
# t1 = MyThread(generate_df, args=(3, 5))
# t1.start()
# t1.join()
# res1 = t1.get_result()
# print(res1)

# list1 = ['601001', '601318', '603337', '300642', '300685', '300418', '002585', '002833']
    code1 = '601318'
#     df1 = generate_df1()
# print(df1)

    # t2 = Thread(target = generate_df1() )
    # t2.start()
    # t2.join()
    @timer()
    def generate_df2():
        for i in range(10):
            generate_df1()

    @timer()
    def generate_df3():
        thread_list = []
        for i in range(10):
            t = Thread(target=generate_df1(), args=())
            thread_list.append(t)
            t.start()
        e = len(thread_list)

        while True:
            for th in thread_list:
                if not th.is_alive():
                    e -= 1
            if e <= 0:
                break

    @timer()
    def generate_df4():
        process_list = []
        for x in range(10):
            p = Process(target=generate_df1())
            process_list.append(p)
            p.start()
        e = process_list.__len__()

        while True:
            for pr in process_list:
                if not pr.is_alive():
                    e -= 1
            if e <= 0:
                break

    generate_df2()
    generate_df3()
    generate_df4()