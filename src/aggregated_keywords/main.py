from keyword_extraction import ChineseKeywordExtractor
from data_processing import DataProcessor
from aggregation import Aggregator


def main():
    # 文件路径
    raw_data_path = r"D:\pythonProject\数字化营销\data\raw\11月VIP特价直充订单表.xlsx"
    result_path = r"D:\pythonProject\数字化营销\data\processed\aggregated_keywords.csv"
    stop_words_path = "stopwords.txt"

    # 加载和预处理数据
    processor = DataProcessor(raw_data_path)
    df = processor.load_data()
    df = processor.preprocess_data(df)
    # 提取关键词
    extractor = ChineseKeywordExtractor(stop_words_path=stop_words_path)  # 在这里传递停用词路径
    df['关键词'] = df['商品标题'].apply(extractor.extract_keywords)  # 这里只传递text参数
    # 将关键词列展开为多行
    df = df.explode('关键词')

    # 聚合数据
    aggregator = Aggregator()
    result = aggregator.aggregate(df, '关键词', '商品一级类目名称')

    # 保存结果
    result.to_csv(result_path, index=False)
    print(f"结果已保存到 {result_path}")


if __name__ == "__main__":
    main()
