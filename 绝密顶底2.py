# 根据一组股票的名称，获取股票的抄底逃顶信号
import pandas as pd
import os
import time
import datetime
import warnings
import akshare as ak

from threading import Thread
from MyTT import *

pd.set_option('display.max_columns',None)  #显示所有列
pd.set_option('display.max_rows',None)  #显示所有行
pd.set_option('max_colwidth',100)  #设置value的显示长度
pd.set_option('display.width',1000)  #设置1000列时才换行
warnings.filterwarnings("ignore")  # 抑制警告

#一个计算函数运行时长的装饰器
def timer(func):
    def wrapper(*args, **kw):
        # start = time.perf_counter()
        print('我准备开始执行：{} 函数了:'.format(func.__name__))
        # func(*args, **kw)         # 真正执行的是这行。
        t1=time.time()
        func(*args, **kw)
        t2=time.time()
        cost_time = t2-t1
        print("花费时间：{}秒".format(cost_time))
        print('我执行完了')
    return wrapper
# 输出数据分析日期
def print_date(date):
    year = pd.to_datetime(date).year
    month = pd.to_datetime(date).month
    day = pd.to_datetime(date).day
    print("分析日期是{}年{}月{}日".format(year, month, day))


# 定义装饰器
# def timer(func):
#     def wrapper(*args, **kw):
#         start = time.perf_counter()
#         print('我准备开始执行：{} 函数了'.format(func.__name__))
#         return func(*args, **kw)
#         end = time.perf_counter()
#         print('我执行完了，函数运行时间: {}'.format(end - start))
#     return wrapper
# def timer(mode):
#     def wrapper(func):
#         def deco(*args, **kw):
#             type = kw.setdefault('type', None)
#             t1=time.time()
#             func(*args, **kw)
#             t2=time.time()
#             cost_time = t2-t1
#             print("{}-{}花费时间：{}秒".format(mode, type,cost_time))
#         return deco
#     return wrapper

#获取证券数据库信息
def get_security_info_df():
    if os.path.exists('证券数据.xlsx'):
        df = pd.read_excel('证券数据.xlsx',dtype={'代码': 'object'}) #读取数据，采用dtype保证原str不被转为int
    else:
        security_info_df = pd.concat([ak.stock_zh_a_spot_em()[['代码', '名称']],
                                      ak.fund_etf_spot_em()[['代码', '名称']]], axis=0)  # 获取所有证券名称和证券代码的df
        security_info_df['名称'] = security_info_df['名称'].str.replace(' ', '')
        # print(security_info_df)
        # security_info_df.to_csv('证券数据.csv')
        security_info_df.to_excel ('证券数据.xlsx')
        df = pd.read_excel(open('证券数据.xlsx', 'rb'),dtype={'代码': 'object'})
    return df

def security_name_to_code(base_df, name_list):
    df1 = base_df[base_df['名称'].isin(name_list)]  # yeah! 终于找到解决方案了
    df1.drop_duplicates('名称', inplace=True)
    code_list = df1['代码'].tolist()
    return code_list

#将证券名称转为证券代码
def security_name_to_code1(base_df, name_list):
    code_list = []
    name_base_list = base_df['名称'].tolist()  # 获取所有证券名称的列表
    code_base_list = base_df['代码'].tolist()  # 获取所有证券代码的列表
    base_info_dic = dict(zip(name_base_list, code_base_list))  # 以股票名称为KEY,以股票代码为VALUE,生成字典备用
    for i in range(0, len(name_list)):
        name = name_list[i]
        code = base_info_dic.get(name)
        code_list.append(code)
    return code_list

def juemi_dingdi(code_list, Period, Start_Date, End_Date):
    security_df = pd.DataFrame()  # 建立一个空的df,用以保存数据
    for security_code in code_list:  # 逐个获取每支证券的df
        if (security_code[0] == '0' or security_code[0] == '3' or security_code[0] == '6'):
            df = ak.stock_zh_a_hist(security_code, period=Period, start_date=Start_Date,
                                    end_date=End_Date, adjust='qfq')
        else:
            df = ak.fund_etf_hist_em(security_code, period= Period, start_date=Start_Date,
                                     end_date=End_Date, adjust='qfq')

        # -------改成MyTT的格式 -------------
        CLOSE = df['收盘'].values
        OPEN = df['开盘'].values  # 基础数据定义，只要传入的是序列都可以
        HIGH = df['最高'].values
        LOW = df['最低'].values

        # 根据通达信绝密顶底公司改写
        Var1 = (CLOSE - LLV(LOW, 36)) / (HHV(HIGH, 36) - LLV(LOW, 36)) * 100
        Var2 = SMA(Var1, 3, 1)
        Var3 = SMA(Var2, 3, 1)
        Var4 = SMA(Var3, 3, 1)
        Var6 = (CROSS(Var3, Var4)) & (Var3 < 20)  # “抄底”序列
        Var7 = (CROSS(Var4, Var3)) & (Var3 > 80)  # “逃顶”序列

        security_df1 = pd.DataFrame({'证券代码': security_code,
                                     "抄底": Var6, "逃顶": Var7})  # 生成一个具有抄底和逃顶信号的dataframe
        security_df1 = security_df1.iloc[-1:]  # 获取End_Date的抄底逃顶信号
        security_df = security_df.append(security_df1)  # 初步输出一个具有抄底逃顶信号的df
    # security_df = pd.concat([security_df, security_name_df.set_index(security_df.index)],
    #                         axis=1)  # 将不同索引的DataFrame拼接在一起,生成df2
    security_df = pd.DataFrame(security_df, columns=['证券代码', '抄底', '逃顶'])


    security_df.set_index('证券代码', inplace=True)
    security_df = security_df.replace(True, '1')  # 为了直观的展示数据，将True用1表示，将False用0表示
    security_df = security_df.replace(False, '0')
    chaodi_df = security_df.query("'1' == 抄底")
    taoding_df = security_df.query("'1' == 逃顶")
    chaodi_number = chaodi_df.shape[0]
    taoding_number = taoding_df.shape[0]

    print("抄底股票数量是" + str(chaodi_number) + "个")
    print("逃顶股票数量是" + str(taoding_number) + "个")

    security_df = pd.concat([chaodi_df, taoding_df], axis=0)
    return security_df

def main():
    start = time.perf_counter()
    security_info_df = get_security_info_df()  #获得基础证券信息
    security_name_df = pd.read_excel(open('D:\股票整理\证券.xlsx', 'rb'),
                                     sheet_name='自选股', index_col=None)  # 根据自选股、持仓股，读入股票名称
    security_name_list = security_name_df['证券名称'].tolist()  # 将股票df转换为股票list
    security_code_list = security_name_to_code(security_info_df, security_name_list)

    end_date = datetime.datetime.now()  # 获取本地时间，标准时间格式，pd.to_datetime()可以将字符串转为标准时间格式
    start_date = end_date - datetime.timedelta(days=200)  # 本地时间减去190天为开始时间
    end_date = end_date.strftime('%Y-%m-%d')  # 将结束时间由标准时间格式转为字符串
    start_date = start_date.strftime('%Y-%m-%d')  # 将开始时间由标准时间格式转为字符串
    end_date = end_date.replace('-', '')  # 去掉字符串中的'-'
    start_date = start_date.replace('-', '')  # 去掉字符串中的'-'
    # start_date = '20200623'
    # end_date = '20230217'
    print_date(end_date)

    dingdi_df = juemi_dingdi(security_code_list, Period='daily',
                         Start_Date=start_date, End_Date=end_date) #获得绝密顶底df,period={'daily', 'weekly', 'monthly'}
    end = time.perf_counter()
    print('我执行完了，函数运行时间: {}'.format(end - start))
    print(dingdi_df)


if __name__ == '__main__':
    main()
