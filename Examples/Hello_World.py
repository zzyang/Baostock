import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取历史K线数据 ####
"""
日线指标参数（包含停牌证券）
参数名称	        参数描述	        说明
date	        交易所行情日期	格式：YYYY-MM-DD
code	        证券代码	        格式：sh.600000。sh：上海，sz：深圳
open	        今开盘价格	    精度：小数点后4位；单位：人民币元
high	        最高价	        精度：小数点后4位；单位：人民币元
low	            最低价	        精度：小数点后4位；单位：人民币元
close	        今收盘价	        精度：小数点后4位；单位：人民币元
preclose	    昨日收盘价	    精度：小数点后4位；单位：人民币元
volume	        成交数量	        单位：股
amount	        成交金额	        精度：小数点后4位；单位：人民币元
adjustflag	    复权状态	        不复权、前复权、后复权
turn	        换手率	        精度：小数点后6位；单位：%
tradestatus	    交易状态	        1：正常交易 0：停牌
pctChg	        涨跌幅（百分比）	精度：小数点后6位
peTTM	        滚动市盈率	    精度：小数点后6位
psTTM	        滚动市销率	    精度：小数点后6位
pcfNcfTTM	    滚动市现率	    精度：小数点后6位
pbMRQ	        市净率	        精度：小数点后6位
isST	        是否ST	        1是，0否
"""

"""
周、月线指标参数
参数名称	        参数描述	        说明	                                    算法说明
date	        交易所行情日期	格式：YYYY-MM-DD	
code	        证券代码	        格式：sh.600000；sh：上海，sz：深圳	
open	        开盘价格	        精度：小数点后4位；单位：人民币元	
high	        最高价	        精度：小数点后4位；单位：人民币元	
low	            最低价	        精度：小数点后4位；单位：人民币元	
close	        收盘价	        精度：小数点后4位；单位：人民币元	
volume	        成交数量	        单位：股	
amount	        成交金额	        精度：小数点后4位；单位：人民币元	
adjustflag	    复权状态	        不复权、前复权、后复权	
turn	        换手率	        精度：小数点后6位；单位：%	
pctChg	        涨跌幅（百分比）	精度：小数点后6位	                        涨跌幅=[(区间最后交易日收盘价-区间首个交易日前收盘价)/区
"""

"""
5、15、30、60分钟线指标参数(不包含指数)
参数名称	        参数描述	        说明
date	        交易所行情日期	格式：YYYY-MM-DD
time	        交易所行情时间	格式：YYYYMMDDHHMMSSsss
code	        证券代码	        格式：sh.600000。sh：上海，sz：深圳
open	        开盘价格	        精度：小数点后4位；单位：人民币元
high	        最高价	        精度：小数点后4位；单位：人民币元
low	            最低价	        精度：小数点后4位；单位：人民币元
close	        收盘价	        精度：小数点后4位；单位：人民币元
volume	        成交数量	        单位：股
amount	        成交金额	        精度：小数点后4位；单位：人民币元
adjustflag	    复权状态	        不复权、前复权、后复权
"""

"""
参数含义：

code：       股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
fields：     指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。详细指标列表见历史行情指标参数章节，日线与分钟线参数不同。此参数不可为空；
start：      开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
end：        结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
frequency：  数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
adjustflag： 复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。 BaoStock提供的是涨跌幅复权算法复权因子，具体介绍见：复权因子简介或者BaoStock复权因子简介。
"""

rs = bs.query_history_k_data_plus("sh.600000",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2017-06-01', end_date='2017-12-31',
    frequency="d", adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
#### 结果集输出到csv文件 ####
result.to_csv("./Data/history_k_data.csv", encoding="gbk", index=False)
print(result)

#### 登出系统 ####
bs.logout()