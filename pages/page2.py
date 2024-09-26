import streamlit as st
import numpy as np
from hw1 import *
import re
import pandas as pd

st.set_page_config(
    page_title = "page1",
    initial_sidebar_state = "collapsed"
)

files = st.session_state["multi"]
keyword = st.session_state["host_keyword"]
color = st.session_state["host_color"]

files = [item.split(" ")[1] for item in files]

length = len(st.session_state["multi"])
cols = st.columns(length)

for col, file in zip(cols, files):
    with col:
        title, journal, abstracts, pmid, full_name = extractcontent(file)
        hightlight_title = highlight(title, keyword, color)
        
        st.markdown(f"<h1 style = 'text-align: center; font-size: 40px'>{hightlight_title}</h1>", unsafe_allow_html=True)
        st.markdown(f"Journal: {journal}", unsafe_allow_html=True)
        
        name_list = ""
        for i, name in enumerate(full_name):
            name_list += name
            if i < len(full_name) - 1: name_list += ", "

        st.markdown(f"Author: {name_list}", unsafe_allow_html=True)
        
        for abstract in abstracts:
            content = ''.join(abstract.itertext())
            highlight_content = highlight(content, keyword, color)
            st.markdown(f"{highlight_content}", unsafe_allow_html=True)