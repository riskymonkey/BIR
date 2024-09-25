import streamlit as st
import numpy as np
from hw1 import *
import pandas as pd

st.set_page_config(
    page_title = "host page",
    initial_sidebar_state = "collapsed"
)

if 'host_keyword' not in st.session_state:
    st.session_state.host_keyword = ''

st.title("A simple keyword searching!")

with st.sidebar.expander("Searching Mode"):
    mode = st.radio("mode type", ["Default", "PMID"])

keyword = st.text_input("Enter a keyword")
#color = st.color_picker('Choose color', '#00f900')
color = "red"

st.session_state["host_color"] = color
if keyword:
    st.session_state["host_keyword"] = keyword

if st.session_state["host_keyword"]: 
    result, file_name = searchtitle(st.session_state["host_keyword"], color, mode)
    if len(result) != 0:
        for i, title in enumerate(result):
            sentence = f"{i+1}: " + title
            params = {"file_name": file_name[i], "keyword": keyword, "color": color}
            st.markdown(f"[{sentence}](page?name={params["file_name"]}&keyword={params["keyword"]}&color={params["color"]})", unsafe_allow_html=True)
            with st.expander("Show abstract"):
                sentence_cnt, word_cnt, letter_cnt, ascii_cnt, non_ascii = file_statistic(file_name[i], st.session_state["host_keyword"], st.session_state["host_color"])
                data = {
                    'Metric': ['Sentence Count', 'Word Count', 'Character Count', 'ASCII Count', 'Non-ASCII Count'],
                    'Number': [sentence_cnt, word_cnt, letter_cnt, ascii_cnt, non_ascii]
                }
                df = pd.DataFrame(data)
                st.write(df)
            #st.page_link("pages/page.py")
    else:
        st.write("Oops! there is nothing found")

# uploaded file
with st.sidebar.expander("Upload File"):
    uploaded_file = st.file_uploader("File", type=["txt", "csv", "pdf", "xml", "xlsx"])

    if uploaded_file:
        uploadfile(uploaded_file)

with st.sidebar.expander("File List"):
    showlist()
