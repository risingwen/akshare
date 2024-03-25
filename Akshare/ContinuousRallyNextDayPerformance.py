import os
import pandas as pd

data_dir = './stock_data'
results = []

# 遍历数据目录下的所有文件
for file_path in os.listdir(data_dir):
    full_path = os.path.join(data_dir, file_path)
    if not os.path.isfile(full_path):
        continue

    try:
        df = pd.read_csv(full_path)
        if df.empty:
            continue

        # 假设CSV文件中包含'日期', '涨跌幅'等列
        # 检查连续两天涨幅是否都在15个点以上
        df['前日涨幅'] = df['涨跌幅'].shift(-1)  # 获取前一日的涨跌幅
        for index in range(len(df) - 2):  # 避免越界，因为需要访问index+2的数据
            # 检查连续两日涨幅是否满足条件
            if df.iloc[index]['涨跌幅'] > 15 and df.iloc[index + 1]['前日涨幅'] > 15:
                next_day_performance = df.iloc[index + 2]['涨跌幅']  # 获取次日涨跌幅
                stock_code, stock_name = os.path.basename(full_path).split('_')[:2]
                date = df.iloc[index + 2]['日期']  # 获取次日日期
                results.append((stock_code, stock_name, date, next_day_performance))

    except pd.errors.EmptyDataError:
        print(f"无法解析文件（可能是空的或格式不正确）: {full_path}")

# 打印结果
print("连续两天涨幅超过15%的股票及其次日涨跌幅如下：")
for result in results:
    print(f"股票代码: {result[0]}, 股票名称: {result[1]}, 日期: {result[2]}, 次日涨跌幅: {result[3]:.2f}%")
