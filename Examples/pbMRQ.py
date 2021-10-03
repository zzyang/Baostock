'''

@Description: 在指定日期从全市场中选择最低市盈率的证券
@Author: Andy Yang
@Date: 2021-10-03
@LastEditTime: 2021-10-03
@Comment:
####
hello_world
'''

import pandas as pd
import baostock as bs

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond error_msg:' + lg.error_msg)

# 获取某一天的全市场的证券和指数代码
rs = bs.query_all_stock(day="2021-09-30")
print('query_all_stock respond error_code:' + rs.error_code)
print('query_all_stock respond error_msg:' + rs.error_msg)

# 股票代码集
code_list = []

# 数据集
data_list = []

while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    code_list.append(rs.get_row_data()[0])
# print(code_list)

# df = pd.DataFrame()

# 获取证券的peTTM的历史数据
for code in code_list:

    rs = bs.query_history_k_data_plus(code, "date,code,pbMRQ",
                                start_date='2021-09-30', end_date='2021-09-30',
                                frequency="d", adjustflag="3")

    if rs.error_code == '0':
        result = rs.get_row_data()
 
            # 删除pe为0的证券或指数
        if float(result[2]) != 0:
            data_list.append(result)

df = pd.DataFrame(data_list, columns=rs.fields)
# 结果集输出到csv文件
df.to_csv("./Data/history_A_stock_k_data.csv", index=False)
df['pbMRQ'] = df['pbMRQ'].astype(float)

# 以peTTM进行升序排序
df_sortby_peTTM = df.sort_values(by='pbMRQ')
df_sortby_peTTM.to_csv("./Data/history_A_stock_k_data2.csv", index=False)
print("当天PB最小的证券: " + df_sortby_peTTM.iloc[0][1])

# 登出系统
bs.logout()