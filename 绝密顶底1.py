# 根据一组股票的名称，获取股票的抄底逃顶信号
import pandas as pd
import time
import warnings
import akshare as ak

from MyTT import *

#显示所有列
pd.set_option('display.max_columns',None)
#显示所有行
pd.set_option('display.max_rows',None)
#设置value的显示长度
pd.set_option('max_colwidth',100)
#设置1000列时才换行
pd.set_option('display.width',1000)
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

security_name_df = pd.read_excel(open('D:\股票整理\证券.xlsx', 'rb'),
                              sheet_name='自选股', index_col= None)  # 读入股票名称数据
#stock_name_list = stock_name_df.iloc[:,0].tolist() #将股票df转换为股票list
security_name_list = security_name_df['证券名称'].tolist() #将股票df转换为股票list
# print(stock_name_list)
# print(security_name_list)
# stock_df = ak.stock_zh_a_spot_em()
# stock_info_df = stock_df[['代码','名称']]
# print(stock_info_df.head())
# fund_df = ak.fund_etf_spot_em()[['代码','名称']]
# print(fund_df)

security_info_df = pd.concat([ak.stock_zh_a_spot_em()[['代码','名称']],
                             ak.fund_etf_spot_em()[['代码','名称']]], axis=0)  #获取所有证券名称和证券代码的df

# df = security_info_df[security_info_df['名称'] == security].index.item() for security  in security_name_list
# print(df)

def security_name_to_code(security_name_list):
    df = pd.DataFrame()
    for security in security_name_list:
        df = df.append(security_info_df[security_info_df['名称'] == security])
    df.drop_duplicates('名称', inplace=True)
    stock_code_list = df['代码'].tolist() #删除重复元素所在行
    return stock_code_list

list1 = security_name_to_code(security_name_list)

print(list1)
# df2 = ak.fund_etf_spot_em()[['代码','名称']]
# df2.to_csv('fund.csv')