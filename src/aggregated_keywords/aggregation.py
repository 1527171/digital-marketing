# 数据聚合
# 根据商品一级类目名称对关键词进行二级聚合。
# 输出聚合后的数据。

class Aggregator:
    def aggregate(self, df, keyword_column, category_column):
        # 按类目和关键词分组，统计支付金额总和和出现次数
        aggregated = df.groupby([category_column, keyword_column]).agg(
            支付金额总和=('支付金额（元）', 'sum'),
            出现次数=(keyword_column, 'size')
        ).reset_index()
        return aggregated
