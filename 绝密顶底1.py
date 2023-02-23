# 根据一组股票的名称，获取股票的抄底逃顶信号
import pandas as pd
import os
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
# def timer(func):
#     def wrapper(*args, **kw):
#         start = time.perf_counter()
#         print('我准备开始执行：{} 函数了:'.format(func.__name__))
#         # 真正执行的是这行。
#         func(*args, **kw)
#
#         end = time.perf_counter()
#         print('我执行完了，函数运行时间: {}'.format(end - start))
#     return wrapper

security_name_df = pd.read_excel(open('D:\股票整理\证券.xlsx', 'rb'),
                              sheet_name='自选股', index_col= None)  # 读入股票名称数据
#stock_name_list = stock_name_df.iloc[:,0].tolist() #将股票df转换为股票list
security_name_list = security_name_df['证券名称'].tolist() #将股票df转换为股票list


print(security_name_list)
# stock_df = ak.stock_zh_a_spot_em()
# stock_info_df = stock_df[['代码','名称']]
# print(stock_info_df.head())
# fund_df = ak.fund_etf_spot_em()[['代码','名称']]
# print(fund_df)
security_info_df = pd.concat([ak.stock_zh_a_spot_em()[['代码', '名称']],
                              ak.fund_etf_spot_em()[['代码', '名称']]], axis=0)  # 获取所有证券名称和证券代码的df
security_info_df['名称'] = security_info_df['名称'].str.replace(' ', '')

df1 = security_info_df[security_info_df['名称'].isin (security_name_list)]  #yeah! 终于找到解决方案了
df1.drop_duplicates('名称', inplace=True)
print(df1)
# def get_security_base():
#     security_info_df = pd.concat([ak.stock_zh_a_spot_em()[['代码', '名称']],
#                                   ak.fund_etf_spot_em()[['代码', '名称']]], axis=0)  # 获取所有证券名称和证券代码的df
#     security_info_df['名称'] = security_info_df['名称'].str.replace(' ', '')
#     security_info_df.to_csv('证券数据.csv')
#     return security_info_df

# if os.path.exists('证券数据.csv'):
#     security_info_df = pd.read_csv('证券数据.csv')
# else:
#     security_info_df = get_security_base()

security_name_base = security_info_df['名称'].tolist()  # 获取所有证券名称的列表
security_code_base = security_info_df['代码'].tolist()  # 获取所有证券代码的列表
security_info_dic = dict(zip(security_name_base, security_code_base))  # 以股票名称为KEY,以股票代码为VALUE,生成字典备用

# code_list = []
# for i in range(0, len(security_name_list)):
#     name = security_name_list[i]
#     code = security_info_dic.get(name)
#     code_list.append(code)
#
# print(code_list)
# code_list = []
# for i in range(0, len(security_name_list)):
#     name = security_name_list[i]
#     code = security_info_dic.get(name)
#     code_list.append(code)
# print(code_list)

# @timer
def security_name_to_code1(base_df,name_list):
    code_list = []
    name_base_list = base_df['名称'].tolist()  # 获取所有证券名称的列表
    code_base_list = base_df['代码'].tolist()  # 获取所有证券代码的列表
    base_info_dic = dict(zip(name_base_list, code_base_list))  # 以股票名称为KEY,以股票代码为VALUE,生成字典备用
    for i in range(0, len(name_list)):
        # print(i)
        name = name_list[i]
        code = base_info_dic.get(name)
        code_list.append(code)
    # print(code_list)
    return code_list
# @timer
# def security_name_to_code(security_name_list):
#     df = pd.DataFrame()
#     for security in security_name_list:
#         df = df.append(security_info_df[security_info_df['名称'] == security])
#     df.drop_duplicates('名称', inplace=True)
#     stock_code_list = df['代码'].tolist() #删除重复元素所在行
#     return stock_code_list

# def main():
#
#     list2 = security_name_to_code1(security_name_list)
#     print(type(list2))
#
# # if __name__ == '__main__':
#     main()


