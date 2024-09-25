import streamlit as st
import numpy as np
from hw1 import *
import re

st.set_page_config(
    page_title = "page1",
    initial_sidebar_state = "collapsed"
)

#st.title("This is content in the file")
file_name = st.query_params["name"]
keyword = st.query_params["keyword"]
color = st.query_params["color"]
#st.write(file_name)
# tmp = st.session_state["file_name"]
title, journal, abstracts = extractcontent(file_name)

#st.write(title)
hightlight_title = highlight(title, keyword, color)
#st.markdown(f"<h1 style='text-align: center; color: red;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"{hightlight_title}", unsafe_allow_html=True)
#st.write(journal)

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
st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Sentences: {sentence_cnt}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Words: {word_cnt}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Letters: {letter_cnt}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Ascii: {ascii_cnt}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style = 'text-align: center; font-size: 20px'>Non-Ascii: {non_ascii}</h1>", unsafe_allow_html=True)
# for data in tmp:
#     st.write(data)