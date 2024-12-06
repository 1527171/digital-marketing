# 关键词提取模块
# 负责从商品标题提取关键词。
# 使用 NLTK 等自然语言处理工具。
# 包含停用词去除、关键词提取功能
import re
import jieba


class ChineseKeywordExtractor:
    def __init__(self, stop_words_path=None, excluded_words=None):
        # 加载停用词
        self.stop_words = self.load_chinese_stopwords(stop_words_path) if stop_words_path else set()
        self.excluded_words = excluded_words or set()

    def extract_keywords(self, text):
        if not isinstance(text, str):
            return []
        text = self.remove_english_and_whitespace(text)
        # 使用 jieba 进行中文分词
        words = jieba.lcut(text)
        # 过滤掉停用词和无用词
        keywords = [
            word
            for word in words
            if word.strip() not in self.stop_words and word.strip() not in self.excluded_words
        ]
        return keywords

    def load_chinese_stopwords(self, file_path):
        # 加载停用词
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file.readlines())
    def remove_english_and_whitespace(self, text):
        # 使用正则表达式去除英文字符和空白字符
        # 只保留中文字符
        # return re.sub(r'[a-zA-Z0-9\s]', '', text)
        #出去空白字符和数字
        return re.sub(r'[\d\s]', '', text)
