import os
import pandas as pd

# 数据目录和跳过文件列表的路径
data_dir = './stock_data'
skipped_files_path = 'skipped_files.txt'

# 尝试读取跳过文件列表，如果文件存在
if os.path.exists(skipped_files_path):
    with open(skipped_files_path, 'r') as file:
        skipped_files = set(file.read().splitlines())
else:
    skipped_files = set()

selected_stocks = []

# 更新跳过的文件列表
def update_skipped_files(file_path):
    skipped_files.add(file_path)
    with open(skipped_files_path, 'w') as file:
        for skipped_file in skipped_files:
            file.write(f"{skipped_file}\n")

# 遍历数据目录中的文件
for file_path in os.listdir(data_dir):
    full_path = os.path.join(data_dir, file_path)
    if not os.path.isfile(full_path) or full_path in skipped_files:
        continue

    try:
        df = pd.read_csv(full_path)
        if df.empty:
            print(f"跳过空的DataFrame: {full_path}")
            update_skipped_files(full_path)
            continue

        # 从文件名提取股票代码和名称
        stock_code, stock_name = os.path.basename(full_path).split('_')[:2]
        # 计算前一日涨幅
        df['前日涨幅'] = df['涨跌幅'].shift(1)
        # 筛选符合条件的股票
        filtered = df[(df['前日涨幅'] > 9) & (df['成交额'] / 1e8 >= 30) & (df['涨跌幅'] <= -11)]
        
        for index, row in filtered.iterrows():
            if index + 1 < len(df):
                next_day = df.iloc[index + 1]
                next_day_performance = next_day['涨跌幅']
                turnover_in_billion = round(row['成交额'] / 1e8)
                selected_stocks.append((stock_code, stock_name, row['日期'], turnover_in_billion, row['涨跌幅'], row['前日涨幅'], next_day_performance))
                
    except pd.errors.EmptyDataError:
        print(f"无法解析文件（可能是空的或格式不正确）: {full_path}")

# 打印满足条件的股票信息
if selected_stocks:
    print("满足条件的股票，日期，成交额（亿元），跌幅，前一日涨幅及次日的涨跌幅如下：")
    for stock in selected_stocks:
        print(f"股票代码: {stock[0]}, 股票名称: {stock[1]}, 日期: {stock[2]}, 成交额(亿元): {stock[3]}, 跌幅: {stock[4]:.2f}%, 前一日涨幅: {stock[5]:.2f}%, 次日涨跌幅: {stock[6]:.2f}%")
else:
    print('没有找到满足条件的股票。')

