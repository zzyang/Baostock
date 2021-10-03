'''
@Description: 查询季度频率企业杜邦指数信息，提供2007年至今数据。
@Author: Andy Yang
@Date: 2019-10-18
@LastEditTime: 2021-10-03
@Comment: Update Login API

返回数据说明

参数名称	                参数描述	                                算法说明
code	                证券代码
pubDate	                公司发布财报的日期
statDate	            财报统计的季度的最后一天, 比如2017-03-31,
dupontROE	            净资产收益率	                            归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
dupontAssetStoEquity	权益乘数，反映企业财务杠杆效应强弱和财务风险	平均总资产/平均归属于母公司的股东权益
dupontAssetTurn	        总资产周转率，反映企业资产管理效率的指标	    营业总收入/[(期初资产总额+期末资产总额)/2]
dupontPnitoni	        归属母公司股东的净利润/净利润，反映母公司控股子公司百分比。如果企业追加投资，扩大持股比例，则本指标会增加。
dupontNitogr	        净利润/营业总收入，反映企业销售获利率
dupontTaxBurden	        净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额
dupontIntburden	        利润总额/息税前利润，反映企业利息负担，该比值高则税负较低。利润总额/息税前利润=1-利息费用/息税前利润
dupontEbittogr	        息税前利润/营业总收入，反映企业经营利润率，是企业经营获得的可供全体投资人（股东和债权人）分配的盈利占企业全部营收收入的百分比


'''


import baostock as bs
import pandas as pd

'''
@description: 获取指定股票季度频率杜邦指数数据
@param {stock_number:股票代码
        stock_name:股票名称
        year:查询年度,int类型，为空时默认当前年
        quarter:查询季度，int类型，为空时默认当前季度。不为空时只有4个取值：1，2，3，4.
        } 
@return: 
'''
def get_dupont_data(stock_number,stock_name,year,quarter):

    print('==========================================================')
    print("开始进行: "+stock_name+"("+stock_number+")"+"的数据处理")
    print("尝试登陆baostock")
    ## login ##
    # lg=bs.login(user_id="anonymous",password="123456")
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    ##### get stock data #####
    rs = bs.query_dupont_data(code=stock_number, year=year, quarter=quarter)

    print('请求历史数据返回代码:'+rs.error_code)
    print('请求历史数据返回信息:'+rs.error_msg)

    data_list=[]
    while(rs.error_code=='0') & rs.next():
        data_list.append(rs.get_row_data())

    result = pd.DataFrame(data_list, columns=rs.fields)
    bs.logout()
    print(stock_name+"("+stock_number+")"+"的数据处理完成")
    print('==========================================================')
    return result


'''
@description: 获取指定股票数年间季度频率的杜邦指数数据
@param {stock_number:股票代码
        stock_name:股票名称
        start_year:查询起始年度,str类型
        end_year:查询截至年度,str类型
        } 
@return: DataFrame集合类型
'''
def get_dupont_data_year(stock_number,stock_name,start_year,end_year):
    print('==========================================================')
    print("开始进行: "+stock_name+"("+stock_number+")"+"的数据处理")
    print("尝试登陆baostock")

    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    data_list=[]

    for y in range(int(start_year),int(end_year)+1):
        for q in range(1,5):
                ##### get stock data #####
                rs = bs.query_dupont_data(code=stock_number, year=y, quarter=q)
                while(rs.error_code=='0') & rs.next():
                    data_list.append(rs.get_row_data())

    result=pd.DataFrame(data_list, columns=rs.fields)
    bs.logout()
    print(stock_name+"("+stock_number+")"+"的数据处理完成")
    print('==========================================================')
    return result