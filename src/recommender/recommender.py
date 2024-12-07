import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Recommender:
    def __init__(self, user_data):
        """
        初始化推荐系统
        :param user_data: 包含用户行为数据的 DataFrame
        """
        self.user_data = user_data

    def build_user_keyword_matrix(self):
        """
        构建用户-关键词矩阵
        :return: 用户-关键词矩阵 (DataFrame)
        """
        return self.user_data.pivot_table(
            index='用户账号（ID）', columns='关键词', values='出现次数', aggfunc='sum', fill_value=0
        )

    def build_item_keyword_matrix(self):
        """
        构建商品-关键词矩阵
        :return: 商品-关键词矩阵 (DataFrame)
        """
        exploded_data = self.user_data.copy()
        exploded_data = exploded_data[['商品ID', '关键词', '出现次数']].drop_duplicates()
        return exploded_data.pivot_table(
            index='商品ID', columns='关键词', values='出现次数', aggfunc='sum', fill_value=0
        )

    def calculate_user_similarity(self, user_keyword_matrix):
        """
        计算用户相似度矩阵
        :param user_keyword_matrix: 用户-关键词矩阵
        :return: 用户相似度矩阵 (DataFrame)
        """
        user_similarity = cosine_similarity(user_keyword_matrix)
        return pd.DataFrame(user_similarity,
                            index=user_keyword_matrix.index,
                            columns=user_keyword_matrix.index
                        )

    def calculate_item_similarity(self, item_keyword_matrix):
        """
        计算商品相似度矩阵
        :param item_keyword_matrix: 商品-关键词矩阵
        :return: 商品相似度矩阵 (DataFrame)
        """
        item_similarity = cosine_similarity(item_keyword_matrix)
        return pd.DataFrame(item_similarity,
                            index=item_keyword_matrix.index,
                            columns=item_keyword_matrix.index
                        )

    def recommend_items_user_based(self, user_id, user_keyword_matrix, user_similarity_df, data, top_n=5):
        """
        基于用户的协同过滤推荐商品
        :param user_id: 目标用户ID
        :param user_keyword_matrix: 用户-关键词矩阵
        :param user_similarity_df: 用户相似度矩阵
        :param data: 用户数据
        :param top_n: 推荐的商品数
        :return: 推荐商品列表
        """
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:top_n + 1]
        similar_user_items = data[data['用户账号（ID）'].isin(similar_users)]['商品ID'].explode()
        recommended_items = similar_user_items.value_counts().head(top_n)
        return recommended_items.index.tolist()

    def recommend_items_item_based(self, user_id, item_keyword_matrix, item_similarity_df, data, top_n=5):
        """
        基于商品的协同过滤推荐商品
        :param user_id: 目标用户ID
        :param item_keyword_matrix: 商品-关键词矩阵
        :param item_similarity_df: 商品相似度矩阵
        :param data: 用户数据
        :param top_n: 推荐的商品数
        :return: 推荐商品列表
        """
        user_items = data[data['用户账号（ID）'] == user_id]['商品ID'].explode().unique()
        similar_items = pd.Series(dtype=float)
        for item in user_items:
            if item in item_similarity_df.index:
                similar_items = similar_items.add(item_similarity_df[item], fill_value=0)
        recommended_items = similar_items.sort_values(ascending=False).head(top_n).index.tolist()
        return recommended_items

    def recommend_items_combined(self, user_id, user_keyword_matrix, item_keyword_matrix, user_similarity_df,
                                 item_similarity_df, data, top_n=5, alpha=0.5):
        """
        结合用户和商品相似度的推荐算法
        :param user_id: 目标用户ID
        :param user_keyword_matrix: 用户-关键词矩阵
        :param item_keyword_matrix: 商品-关键词矩阵
        :param user_similarity_df: 用户相似度矩阵
        :param item_similarity_df: 商品相似度矩阵
        :param data: 用户数据
        :param top_n: 推荐的商品数
        :param alpha: 用户和商品相似度的权重 (0.0-1.0)
        :return: 推荐商品列表
        """
        # 用户协同过滤推荐
        user_based_recommendations = pd.Series(self.recommend_items_user_based(
            user_id, user_keyword_matrix, user_similarity_df, data, top_n * 2
        ))

        # 商品协同过滤推荐
        item_based_recommendations = pd.Series(self.recommend_items_item_based(
            user_id, item_keyword_matrix, item_similarity_df, data, top_n * 2
        ))

        # 合并两种推荐结果
        combined_recommendations = pd.concat([user_based_recommendations, item_based_recommendations]).value_counts()

        # 加权排序并返回结果
        weighted_recommendations = combined_recommendations * alpha + item_based_recommendations.value_counts() * (
                    1 - alpha)
        return weighted_recommendations.sort_values(ascending=False).head(top_n).index.tolist()

    def recommend_items_random(self, user_id, data, top_n=5):
        """
        随机推荐商品
        :param user_id: 目标用户ID
        :param data: 用户数据
        :param top_n: 推荐的商品数
        :return: 推荐商品列表
        """
        unique_items = data['商品ID'].str.explode().unique()
        return np.random.choice(unique_items, size=top_n, replace=False).tolist()

    def recommend_items_popularity(self, data, top_n=5):
        """
        基于流行度的推荐算法
        :param data: 用户数据
        :param top_n: 推荐的商品数
        :return: 推荐商品列表
        """
        popular_items = data['商品ID'].str.explode().value_counts()
        return popular_items.head(top_n).index.tolist()


def preprocess_text(text):
    """
    对文本进行分词和去除停用词
    """
    # 使用jieba进行分词
    words = jieba.lcut(text)
    return " ".join(words)


# 将文档内容转换为TF-IDF向量
def documents_to_tfidf_matrix(documents):
    """
    将文档内容转换为TF-IDF向量矩阵
    """
    # 对文档内容进行预处理
    preprocessed_docs = {key: preprocess_text(value) for key, value in documents.items()}
    # 使用TF-IDF向量化器
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_docs.values()).toarray()
    # 创建一个字典来映射文档ID到其对应的TF-IDF向量索引
    doc_to_index = {key: idx for idx, key in enumerate(documents.keys())}
    return tfidf_matrix, doc_to_index


# 基于内容的推荐函数
def content_based_recommendation(doc_id, documents, top_n=2):
    """
    根据文档内容的相似性进行推荐

    参数:
    doc_id (int): 要推荐的文档的ID
    documents (dict): 文档ID到文本内容的映射
    top_n (int): 要推荐的文档数量（默认2）

    返回:
    list: 推荐文档ID的列表
    """
    # 将文档内容转换为TF-IDF向量矩阵
    tfidf_matrix, doc_to_index = documents_to_tfidf_matrix(documents)

    # 获取要推荐的文档的TF-IDF向量索引
    target_index = doc_to_index[doc_id]

    # 计算所有文档与目标文档的余弦相似度
    similarities = []
    for idx, (doc_key, _) in enumerate(doc_to_index.items()):
        if idx != target_index:  # 不推荐相同的文档
            similarity = \
                cosine_similarity(tfidf_matrix[target_index].reshape(1, -1), tfidf_matrix[idx].reshape(1, -1))[0][0]
            similarities.append((doc_key, similarity))

    # 根据相似度排序
    similarities.sort(key=lambda x: x[1], reverse=True)

    # 返回前top_n个推荐文档的ID
    return [doc_id_tuple[0] for doc_id_tuple in similarities[:top_n]]
