from pathlib import Path
import pandas as pd
import numpy as np
from recommender import Recommender


def select_usr(series, n=5):
    """
    随机挑选 series 中的 n 个用户 ID。
    :param series: 用户 ID 的 Pandas Series
    :param n: 需要挑选的用户数量
    :return: 随机挑选的用户 ID 列表
    """
    return np.random.choice(series.unique(), size=n, replace=False).tolist()


def save_output(user_recommendations):
    """
    将用户推荐的商品保存为 CSV 文件。
    :param user_recommendations: 包含推荐数据的 DataFrame
    """
    output_path = Path(__file__).resolve().parent.parent.parent / "data" / "result" / "recommendations.csv"
    user_recommendations.to_csv(output_path, index=False, encoding='utf-8')
    print(f"推荐结果已保存到 {output_path}")


def get_id(path, user_id, recommendations):
    """
    根据用户 ID 和推荐商品 ID，从 result_new.xlsx 中查找商品介绍。
    :param path: result_new.xlsx 文件路径
    :param user_id: 用户 ID
    :param recommendations: 推荐的商品 ID 列表
    :return: 包含用户账号、商品介绍和商品 ID 的列表
    """
    # 读取数据
    df = pd.read_csv(path)

    # 查找用户的推荐商品信息
    user_recommendations = []
    for item_id in recommendations:
        match = df[(df['商品ID'] == item_id)]
        if not match.empty:
            user_recommendations.append({
                "用户账号（ID）": user_id,
                "商品名称": match['商品名称'].iloc[0],
                "商品类型": match['商品类型'].iloc[0],
                "商品介绍": match['商品介绍'].iloc[0],
                "商品ID": item_id
            })
    return user_recommendations


def main():
    base_dir = Path(__file__).resolve().parent.parent.parent  # 定位到项目的根目录
    processed_path = base_dir / "data" / "processed" / "aggregated_keywords.csv"
    result_new_path = base_dir / "data" / "processed" / "user_product_allocation.csv"

    # 读取处理后的数据
    aggregated_df = pd.read_csv(processed_path)

    # 初始化推荐器
    recommender = Recommender(aggregated_df)
    user_keyword_matrix = recommender.build_user_keyword_matrix()
    item_keyword_matrix = recommender.build_item_keyword_matrix()

    # 计算用户和商品相似度
    user_similarity_df = recommender.calculate_user_similarity(user_keyword_matrix)
    item_similarity_df = recommender.calculate_item_similarity(item_keyword_matrix)

    # 随机挑选用户进行推荐
    selected_users = select_usr(aggregated_df['用户账号（ID）'], n=5)
    recommendations_list = []

    for user_id in selected_users:
        recommendations = recommender.recommend_items_combined(
            user_id,
            user_keyword_matrix,
            item_keyword_matrix,
            user_similarity_df,
            item_similarity_df,
            aggregated_df,
            top_n=10
        )
        print(f"为用户 {user_id} 推荐的商品: {recommendations}")

        # 根据推荐商品获取商品介绍
        user_recommendations = get_id(result_new_path, user_id, recommendations)
        recommendations_list.extend(user_recommendations)

    # 转换为 DataFrame 并保存结果
    user_recommendations_df = pd.DataFrame(recommendations_list)
    save_output(user_recommendations_df)


if __name__ == "__main__":
    main()
