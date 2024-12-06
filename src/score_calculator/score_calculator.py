class TrafficScoreCalculator:
    def calculate(self, df, keyword_column, category_column, amount_column):
        """
        计算每个关键词和类目对应的流量值分数

        :param df: 聚合后的 DataFrame，包含关键词、类目和支付金额
        :param keyword_column: 关键词列名
        :param category_column: 类目列名
        :param amount_column: 支付金额列名
        :return: 添加了“流量值分数”列的 DataFrame
        """
        # 按类目分组，计算每个类目的总支付金额
        category_totals = df.groupby(category_column)[amount_column].transform('sum')

        # 计算流量值分数
        df['流量值分数'] = (df[amount_column] / category_totals) * 100

        return df
