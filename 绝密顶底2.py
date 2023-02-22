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
    if os.path.exists('证券数据.xlsx'):
        df = pd.read_excel('证券数据.xlsx')
    else:
        security_info_df = pd.concat([ak.stock_zh_a_spot_em()[['代码', '名称']],
                                      ak.fund_etf_spot_em()[['代码', '名称']]], axis=0)  # 获取所有证券名称和证券代码的df
        security_info_df['名称'] = security_info_df['名称'].str.replace(' ', '')
        # print(security_info_df)
        # security_info_df.to_csv('证券数据.csv')
        security_info_df.to_excel ('证券数据.xlsx')
        df = pd.read_excel(open('证券数据.xlsx', 'rb'))
    return df

#证券名称转化为证券代码
# @timer
def security_name_to_code1(base_df,name_list):
    code_list = []
    name_base_list = base_df['名称'].tolist()  # 获取所有证券名称的列表
    code_base_list = base_df['代码'].tolist()  # 获取所有证券代码的列表
    base_info_dic = dict(zip(name_base_list, code_base_list))  # 以股票名称为KEY,以股票代码为VALUE,生成字典备用
    for i in range(0, len(name_list)):
        name = name_list[i]
        code = base_info_dic.get(name)
        code_list.append(code)
    return code_list

def main():
    security_info_df = get_security_info_df()
    security_name_df = pd.read_excel(open('D:\股票整理\证券.xlsx', 'rb'),
                                     sheet_name='自选股', index_col=None)  # 读入股票名称数据
    security_name_list = security_name_df['证券名称'].tolist()  # 将股票df转换为股票list
    security_code_list = security_name_to_code1(security_info_df, security_name_list)
    print(security_code_list)
    # stock_individual_info_em_df = ak.stock_individual_info_em(symbol=security_code_list[0])
    # print(stock_individual_info_em_df)

if __name__ == '__main__':
    main()
