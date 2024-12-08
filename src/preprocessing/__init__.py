from pathlib import Path
import pandas as pd
import numpy as np


def load_data(file_path):
    """
    从 Excel 文件中加载数据。
    :param file_path: Excel 文件路径 (Path 对象)
    :return: 用户账号表, 商品表
    """
    user_data = pd.read_excel(file_path, sheet_name="IP地址、用户账号")
    product_data = pd.read_excel(file_path, sheet_name="商品名称、商品ID及商品介绍")
    return user_data, product_data


def parse_categories(text):
    """
    将 '访问商品类型介绍（字节数）' 按分隔符解析为列表。
    :param text: 字符串，包含商品类型
    :return: 商品类型列表
    """
    return text.split("、")


def dynamic_allocation(access_count, access_duration, max_products, smooth_factor=10):
    """
    根据访问次数和访问时长动态分配商品数量。
    :param access_count: 访问次数
    :param access_duration: 访问时长
    :param max_products: 当前类型商品的最大数量
    :param smooth_factor: 平滑因子，用于控制分配数量
    :return: 动态分配的商品数量
    """
    num_products = int(np.ceil((access_count * access_duration) / smooth_factor))
    return min(num_products, max_products)  # 限制商品数量不超过当前类型商品的总数


def assign_products(user_data, product_data):
    """
    为每个用户的每种商品类型动态分配商品。
    :param user_data: 用户账号表 DataFrame
    :param product_data: 商品表 DataFrame
    :return: 包含用户账号、分配商品信息的 DataFrame
    """
    merged_data = []

    for _, user_row in user_data.iterrows():
        # 解析用户访问的商品类型
        user_categories = parse_categories(user_row["访问商品类型介绍（字节数）"])

        for category in user_categories:
            # 从商品表中找到属于该商品类型的商品
            category_products = product_data[product_data["商品类型"] == category]

            # 动态分配商品数量
            max_products = len(category_products)
            num_products = dynamic_allocation(
                access_count=user_row["访问次数（次）"],
                access_duration=user_row["访问时长（时）"],
                max_products=max_products,
                smooth_factor=5000  # 平滑因子可根据需求调整
            )

            # 随机选择商品
            assigned_products = category_products.sample(n=num_products, replace=False)

            # 合并用户与分配商品信息
            for _, product_row in assigned_products.iterrows():
                merged_data.append({
                    "用户账号（ID）": user_row["用户账号（ID）"],
                    "IP地址": user_row["IP地址"],
                    "访问次数（次）": user_row["访问次数（次）"],
                    "访问时长（时）": user_row["访问时长（时）"],
                    "商品名称": product_row["商品名称"],
                    "商品ID": product_row["商品ID"],
                    "商品类型": product_row["商品类型"],
                    "商品介绍": product_row["商品介绍"]
                })

    return pd.DataFrame(merged_data)


def save_output(data, output_path):
    """
    保存分配结果到文件。
    :param data: 包含分配结果的 DataFrame
    :param output_path: 输出文件路径 (Path 对象)
    """
    data.to_csv(output_path, index=False, encoding="utf-8")
    print(f"分配结果已保存到 {output_path}")


def main():
    # 项目根目录
    base_dir = Path(__file__).resolve().parent.parent.parent  # 定位到项目的根目录

    # 文件路径
    file_path = base_dir / "data" / "raw" / "12月8日数据信息.xlsx"
    output_path = base_dir / "data" / "processed" / "user_product_allocation.csv"

    # 加载数据
    user_data, product_data = load_data(file_path)

    # 分配商品
    result_data = assign_products(user_data, product_data)

    # 保存结果
    save_output(result_data, output_path)


if __name__ == "__main__":
    main()
