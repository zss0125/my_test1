# 采用多线程方法对获取股票数据的方法进行测试
import multiprocessing

import pandas as pd
import os
import time
import datetime
import warnings
import akshare as ak
import requests
import multiprocessing as mp


from multiprocessing import Process
from threading import Thread
from MyTT import *

pd.set_option('display.max_columns',None)  #显示所有列
pd.set_option('display.max_rows',None)  #显示所有行
pd.set_option('max_colwidth',100)  #设置value的显示长度
pd.set_option('display.width',1000)  #设置1000列时才换行
warnings.filterwarnings("ignore")  # 抑制警告

#一个计算函数运行时长的装饰器
# def timer(func):
#     def wrapper(*args, **kw):
#         # start = time.perf_counter()
#         print('我准备开始执行：{} 函数了:'.format(func.__name__))
#         # func(*args, **kw)         # 真正执行的是这行。
#         t1=time.time()
#         func(*args, **kw)
#         t2=time.time()
#         cost_time = t2-t1
#         print("花费时间：{}秒".format(cost_time))
#         print('我执行完了')
#     return wrapper
# 输出数据分析日期
def print_date(date):
    year = pd.to_datetime(date).year
    month = pd.to_datetime(date).month
    day = pd.to_datetime(date).day
    print("分析日期是{}年{}月{}日".format(year, month, day))

def timer(mode):
    def wrapper(func):
        def deco(*args, **kw):
            type = kw.setdefault('type', None)
            t1=time.time()
            func(*args, **kw)
            t2=time.time()
            cost_time = t2-t1
            print("{}-{}花费时间：{}秒".format(mode, type,cost_time))
        return deco
    return wrapper

class Exectime():
    def __init__(self, unit: str = 's', e_time: int = None, ):
        self.unit = unit
        self.e_time = e_time
        self.str_f = ''

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            import time as t
            start_time = t.time()
            res = func(*args, **kwargs)
            end_time = t.time()

            exec_time = self.e_time or end_time - start_time

            # exec_time *= 1000
            symbols = {'m': 'Minute', 'h': 'Hour', 'd': 'Day'}
            sy_time = {"Minute": 60, "Hour": 3600, "Day": 86400}

            try:
                if symbols[self.unit]:
                    if symbols[self.unit] == "Minute":
                        exec_time = exec_time / sy_time["Minute"] if exec_time >= sy_time["Minute"] else exec_time
                        unit_f = "Minute"
                    elif symbols[self.unit] == "Hour":
                        exec_time = exec_time / sy_time["Minute"] if exec_time >= sy_time["Minute"] else exec_time
                        unit_f = "Hour"
                    elif symbols[self.unit] == "Day":
                        exec_time = exec_time / sy_time["Minute"] if exec_time >= sy_time["Minute"] else exec_time
                        unit_f = "Day"
            except:
                unit_f = "Second"

            print("FuncName: {} ==> Exec: {:g} {}!\n".format(func.__name__, exec_time, unit_f))

            return res
        return wrapper
# CPU计算密集型
def count(x=1, y=1):
    # 使程序完成150万计算
    c = 0
    while c < 500000:
        c += 1
        x += x
        y += y

# 磁盘读写IO密集型
def io_disk():
    with open("file.txt", "w") as f:
        for x in range(5000000):
            f.write("python-learning\n")

# 网络IO密集型
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
url = "https://www.tieba.com/"

def io_request():
    try:
        webPage = requests.get(url, headers=header)
        html = webPage.text
        return
    except Exception as e:
        return {"error": e}

# 【模拟】IO密集型
def io_simulation():
    df = ak.stock_zh_a_hist(symbol="000001", period="daily",
                                            start_date="20200301", end_date='20220907', adjust="")
    return df
def time_cal(func):
    def inner(*s,**gs):
        time_start = datetime.datetime.now()
        # start = time.perf_counter()
        func(*s,**gs)
        # end = time.perf_counter()
        time_end = datetime.datetime.now()
        print(f"方法名0:{func.__name__}:运行耗时{(time_end - time_start)}s")
        # print(f"方法名1:{func.__name__}:运行耗时{(end - start)}s")
    return inner

#重写一个可以获得返回值的多线程
class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
# class Exectime():
#     def __init__(self, unit: str = 's', e_time: int = None, ):
#         self.unit = unit
#         self.e_time = e_time
#         self.str_f = ''
#
#     def __call__(self, func):
#         def wrapper(*args, **kwargs):
#             import time as t
#             start_time = t.time()
#             res = func(*args, **kwargs)
#             end_time = t.time()
#
#             exec_time = self.e_time or end_time - start_time
#
#             # exec_time *= 1000
#             symbols = {'m': 'Minute', 'h': 'Hour', 'd': 'Day'}
#             sy_time = {"Minute": 60, "Hour": 3600, "Day": 86400}
#
#             try:
#                 if symbols[self.unit]:
#                     if symbols[self.unit] == "Minute":
#                         exec_time = exec_time / sy_time["Minute"] if exec_time >= sy_time["Minute"] else exec_time
#                         unit_f = "Minute"
#                     elif symbols[self.unit] == "Hour":
#                         exec_time = exec_time / sy_time["Minute"] if exec_time >= sy_time["Minute"] else exec_time
#                         unit_f = "Hour"
#                     elif symbols[self.unit] == "Day":
#                         exec_time = exec_time / sy_time["Minute"] if exec_time >= sy_time["Minute"] else exec_time
#                         unit_f = "Day"
#             except:
#                 unit_f = "Second"
#
#             print("FuncName: {} ==> Exec: {:g} {}!\n".format(func.__name__, exec_time, unit_f))
#
#             return res
#         return wrapper

# @Exectime()
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
# @Exectime()
def security_name_to_code(base_df, name_list):
    df1 = base_df[base_df['名称'].isin(name_list)]  # yeah! 终于找到解决方案了
    df1.drop_duplicates('名称', inplace=True)
    code_list = df1['代码'].tolist()
    return code_list
# @Exectime()
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


# @Exectime()
def juemi_dingdi(code_list, Period, Start_Date, End_Date):
    security_df = pd.DataFrame()  # 建立一个空的df,用以保存数据
    thread_list = []
    for security_code in code_list:  # 逐个获取每支证券的df
        # p = Process(target = get_security_info_df())
        if (security_code[0] == '0' or security_code[0] == '3' or security_code[0] == '6'):
            # t1 = Thread(target = ak.stock_zh_a_hist(), args=(security_code, 'daily', '20220101',
            #                         '20230101'))
            # thread_list.append(t1)
            # t1.start()
            # df = t1.get_result()
            df = ak.stock_zh_a_hist(security_code, period=Period, start_date=Start_Date,
                             end_date=End_Date, adjust='qfq')
        else:
            # t1 = Thread(target = ak.fund_etf_hist_em(), args=(security_code, 'daily', '20220101',
            #                         '20230101'))
            # thread_list.append(t1)
            # t1.start()
            # df = t1.get_result()
            df = ak.fund_etf_hist_em(security_code, period= Period, start_date=Start_Date,
                                     end_date=End_Date, adjust='qfq')

    # e = len(thread_list)
    # while True:
    #     for th in thread_list:
    #         if not th.is_alive():
    #             e -= 1
    #     if e <= 0:
    #         break
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
    print(security_df)
    return security_df

# @timer("【单线程】")
# def single_thread(func, type=""):
#     for i in range(10):
#         func()
def get_df():
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily",
                                            start_date="20170301", end_date='20210907', adjust="")


def main():
    start = time.time()
    print('我准备开始执行main()函数了')
    @timer("【单线程】")
    def single_thread(func, type=""):
        for i in range(20):
            func()

    @timer("【多线程】")
    def multi_thread(func, type=""):
        thread_list = []
        for i in range(20):
            t = Thread(target=func, args=())
            thread_list.append(t)
            t.start()
        e = len(thread_list)

        while True:
            for th in thread_list:
                if not th.is_alive():
                    e -= 1
            if e <= 0:
                break

    @timer("【多进程】")
    def multi_process(func, type=""):
        process_list = []
        for x in range(20):
            p = Process(target=func, args=())
            process_list.append(p)
            p.start()
        e = process_list.__len__()

        while True:
            for pr in process_list:
                if not pr.is_alive():
                    e -= 1
            if e <= 0:
                break
    # 单线程
    # single_thread(count, type="CPU计算密集型")
    # single_thread(io_disk, type="磁盘IO密集型")
    # single_thread(io_request, type="网络IO密集型")
    # single_thread(io_simulation, type="模拟IO密集型")
    # multi_thread(io_simulation, type="模拟IO密集型")
    # multi_process(io_simulation, type="模拟IO密集型")


    security_info_df = get_security_info_df()  #获得基础证券信息
    security_name_df = pd.read_excel(open('D:\股票整理\证券.xlsx', 'rb'),
                                     sheet_name='持仓股', index_col=None)  # 根据自选股、持仓股，读入股票名称
    security_name_list = security_name_df['证券名称'].tolist()  # 将股票df转换为股票list
    security_code_list = security_name_to_code1(security_info_df, security_name_list)

    end_date = datetime.datetime.now()  # 获取本地时间，标准时间格式，pd.to_datetime()可以将字符串转为标准时间格式
    start_date = end_date - datetime.timedelta(days=200)  # 本地时间减去190天为开始时间
    end_date = end_date.strftime('%Y-%m-%d')  # 将结束时间由标准时间格式转为字符串
    start_date = start_date.strftime('%Y-%m-%d')  # 将开始时间由标准时间格式转为字符串
    end_date = end_date.replace('-', '')  # 去掉字符串中的'-'
    start_date = start_date.replace('-', '')  # 去掉字符串中的'-'
    # # start_date = '20200623'
    # # end_date = '20230217'
    # print_date(end_date)
    # t1 = Thread(target=juemi_dingdi, args=(security_code_list, 'daily', start_date, end_date))
    # t1.start()
    # t1.join()
    # t2 = Process(target=juemi_dingdi, args=(security_code_list, 'daily', start_date, end_date))
    # t2.start()
    # t2.join()
    # mp = multiprocessing.Pool(60)
    # mplist = []
    # for i in range(0, 60):
    #     mplist.append(
    #         mp.apply_async(
    #             func=juemi_dingdi,
    #             kwds={'code_list':security_code_list, 'Period':'daily', 'Start_Date': start_date,
    #                   'End_Date': end_date}))
    # mp.close()
    # mp.join()



    # dingdi_df = juemi_dingdi(security_code_list, Period='daily',
    #                      Start_Date=start_date, End_Date=end_date) #获得绝密顶底df,period={'daily', 'weekly', 'monthly'}
    # print(dingdi_df)
    # print(security_info_df)
    end = time.time()
    cost_time = end - start
    print("花费时间：{}秒".format(cost_time))
    print('我执行完了')
if __name__ == '__main__':
    main()
