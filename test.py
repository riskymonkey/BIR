import streamlit as st
import numpy as np
from hw1 import *

keyword = "for"
file_name = "X39258374.xml"
#result, file_name, orig = searchtitle(keyword)
title, journal, abstracts = extractcontent(file_name)
for abstract in abstracts:
    content = ''.join(abstract.itertext())
    s_tmp, w_tmp, l_tmp = statistic(content)

text = """
positive predictive value (48.6 vs. 42.4%, P=0.031), and accuracy (55.5 vs. 44.1%, P<0.001) than the IAP 2017 guidelines.
"""

# 定义需要忽略的缩写词的正则表达式（可以根据需要添加更多缩写词）
abbreviations = r'\b(?:\d+\.\d+|e\.g\.|i\.e\.|vs\.|etc\.)'

# 将缩写词中的句号替换为特殊标记，避免被当作句子结尾
modified_text = re.sub(abbreviations, lambda x: x.group(0).replace('.', '<DOT>'), text)
#print(modified_text)

# 使用正则表达式根据句子结尾符号（'.', '!', '?'）进行分割
sentences = re.split(r'[.!?]+', modified_text)

# 去除空白和无效的结果
sentences = [s.strip() for s in sentences if s.strip()]

# 计算句子数量
sentence_count = len(sentences)