import os
import akshare as ak

# 检查目录是否存在，如果不存在，则创建
data_dir = './stock_data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 获取A股股票列表
stock_list = ak.stock_zh_a_spot_em()

# 遍历列表，下载每个股票的数据
for index, row in stock_list.iterrows():
    try:
        stock_code = row['代码']
        # 获取股票的历史行情数据
        stock_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20190101", end_date="20240101", adjust="qfq")
        # 保存数据到CSV文件
        file_path = os.path.join(data_dir, f'{stock_code}_daily.csv')
        stock_df.to_csv(file_path, index=False)
        print(f'{stock_code} 数据下载完成')
    except Exception as e:
        print(f'下载{stock_code}数据时发生错误: {e}')

print('全部股票数据下载完成。')
