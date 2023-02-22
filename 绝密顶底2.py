# 根据一组股票的名称，获取股票的抄底逃顶信号
import pandas as pd
import os
import time
import warnings
import akshare as ak

from MyTT import *

pd.set_option('display.max_columns',None)  #显示所有列
pd.set_option('display.max_rows',None)  #显示所有行
pd.set_option('max_colwidth',100)  #设置value的显示长度
pd.set_option('display.width',1000)  #设置1000列时才换行
warnings.filterwarnings("ignore")  # 抑制警告

#一个计算函数运行时长的装饰器
def timer(func):
    def wrapper(*args, **kw):
        start = time.perf_counter()
        print('我准备开始执行：{} 函数了:'.format(func.__name__))

        # 真正执行的是这行。
        func(*args, **kw)

        end = time.perf_counter()
        print('我执行完了，函数运行时间: {}'.format(end - start))
    return wrapper

#获取证券数据库信息
def get_security_info_df():
    if os.path.exists('证券数据.csv'):
        df = pd.read_csv('证券数据.csv')
    else:
        security_info_df = pd.concat([ak.stock_zh_a_spot_em()[['代码', '名称']],
                                      ak.fund_etf_spot_em()[['代码', '名称']]], axis=0)  # 获取所有证券名称和证券代码的df
        security_info_df['名称'] = security_info_df['名称'].str.replace(' ', '')
        security_info_df.to_csv('证券数据.csv')
        df = pd.read_csv('证券数据.csv')
    return df



def main():
    security_info_df = get_security_info_df()


if __name__ == '__main__':
    main()
