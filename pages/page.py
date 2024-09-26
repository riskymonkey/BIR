import streamlit as st
import numpy as np
from hw1 import *
import re
import pandas as pd

st.set_page_config(
    page_title = "page1",
    initial_sidebar_state = "collapsed"
)

#st.title("This is content in the file")
file_name = st.query_params["name"]
keyword = st.query_params["keyword"]
color = st.query_params["color"]

#file_name = st.session_state["file_name"]
#keyword = st.session_state["keyword"]
#color = st.session_state["color"]

with st.sidebar.expander("test"):
    st.write("test")

title, journal, abstracts, pmid, full_name = extractcontent(file_name)

#st.write(title)
hightlight_title = highlight(title, keyword, color)
#st.markdown(f"<h1 style='text-align: center; color: red;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style = 'text-align: center; font-size: 40px'>{hightlight_title}</h1>", unsafe_allow_html=True)
st.markdown(f"Journal: {journal}", unsafe_allow_html=True)
name_list = ""
for i, name in enumerate(full_name):
    name_list += name
    if i < len(full_name) - 1: name_list += ", "

st.markdown(f"Author: {name_list}", unsafe_allow_html=True)

sentence_cnt = 0
word_cnt = 0
letter_cnt = 0
ascii_cnt = 0

for abstract in abstracts:
    content = ''.join(abstract.itertext())
    highlight_content = highlight(content, keyword, color)
    st.markdown(f"{highlight_content}", unsafe_allow_html=True)
    #st.write(content)
    s_tmp, w_tmp, l_tmp, a_tmp = statistic(content)
    sentence_cnt += s_tmp
    word_cnt += w_tmp
    letter_cnt += l_tmp
    ascii_cnt += a_tmp

letter_cnt += (len(abstracts) - 1)
ascii_cnt += (len(abstracts) - 1)
#st.write("test")
non_ascii = letter_cnt - ascii_cnt
data = {
        'Metric': ['Sentence Count', 'Word Count', 'Character Count', 'ASCII Count', 'Non-ASCII Count'],
        'Number': [sentence_cnt, word_cnt, letter_cnt, ascii_cnt, non_ascii]
}
df = pd.DataFrame(data)

# 使用 CSS 置中顯示 DataFrame
st.write(df)
# st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Sentences: {sentence_cnt}</h1>", unsafe_allow_html=True)
# st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Words: {word_cnt}</h1>", unsafe_allow_html=True)
# st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Letters: {letter_cnt}</h1>", unsafe_allow_html=True)
# st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Ascii: {ascii_cnt}</h1>", unsafe_allow_html=True)
# st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Non-Ascii: {non_ascii}</h1>", unsafe_allow_html=True)
# for data in tmp:
#     st.write(data)