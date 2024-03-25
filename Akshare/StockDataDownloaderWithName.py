import akshare as ak
import os

# 获取A股股票列表
stock_list = ak.stock_zh_a_spot_em()

# 确保有一个目录来存放下载的股票数据
data_dir = './stock_data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 遍历股票列表，下载数据
for index, row in stock_list.iterrows():
    stock_code = row['代码']
    stock_name = row['名称']
    try:
        # 获取股票的历史行情数据
        stock_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20210101", end_date="20240325", adjust="qfq")
        # 你可以选择将股票名称添加为DataFrame的一列
        stock_df['股票名称'] = stock_name
        # 保存数据到CSV文件，文件名中包含股票名称
        file_path = os.path.join(data_dir, f'{stock_code}_{stock_name}_daily.csv')
        stock_df.to_csv(file_path, index=False)
        print(f'{stock_code}({stock_name}) 数据下载完成')
    except Exception as e:
        print(f'下载{stock_code}({stock_name})数据时发生错误: {e}')
