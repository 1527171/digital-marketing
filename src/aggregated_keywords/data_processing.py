# 数据加载与预处理模块
# 负责加载 SQL 数据。
# 数据预处理，例如数据清洗、格式化等。

import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        return pd.read_excel(self.file_path)

    def preprocess_data(self, df):
        # 选择需要的字段
        df = df[['用户账号（ID）','访问次数（次）','访问时长（时）','商品介绍','商品ID']]
        # 处理空值
        df.dropna()
        return df
