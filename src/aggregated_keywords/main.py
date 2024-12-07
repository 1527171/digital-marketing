from keyword_extraction import ChineseKeywordExtractor
from data_processing import DataProcessor
from aggregation import Aggregator
from pathlib import Path


def main():
    # 文件路径
    base_dir = Path(__file__).resolve().parent.parent.parent  # 定位到项目的根目录
    raw_data_path = base_dir / "data" / "raw" / "result_new.xlsx"
    result_path = base_dir / "data" / "processed" / "aggregated_keywords.csv"
    stop_words_path = "stopwords.txt"

    # 加载和预处理数据
    processor = DataProcessor(raw_data_path)
    df = processor.load_data()
    df = processor.preprocess_data(df)

    # 提取关键词
    extractor = ChineseKeywordExtractor(stop_words_path=stop_words_path)
    df['关键词'] = df['商品介绍'].apply(extractor.extract_keywords)
    df = df.explode('关键词')  # 将关键词列展开为多行
    # 聚合数据
    aggregator = Aggregator()
    result = aggregator.aggregate(df,
                                  '关键词',
                                  ['用户账号（ID）','访问次数（次）','访问时长（时）','商品ID','关键词']
                                )

    # 保存结果
    result.to_csv(result_path, index=False, encoding='utf-8')
    print(f"关键词聚合结果已保存到 {result_path}")

if __name__ == "__main__":
    main()
