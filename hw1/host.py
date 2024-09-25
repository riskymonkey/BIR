import streamlit as st
import numpy as np
from hw1 import *

st.set_page_config(
    page_title = "host page",
    initial_sidebar_state = "collapsed"
)

st.sidebar.success("Pages above")
# cells
st.title("A simple keyword searching!")
#mode = st.radio("mode type", ["Num", "No display"])
keyword = st.text_input("Enter a keyword")
color = st.color_picker('Choose color', '#00f900')

#result, file_name, orig = searchtitle(keyword, color)

#st.session_state["file_name"] = file_name
if keyword:
    
    result, file_name = searchtitle(keyword, color)
    if len(result) != 0:
        for i, title in enumerate(result):
            sentence = f"{i+1}: " + title
            params = {"file_name": file_name[i], "keyword": keyword, "color": "red"}
            st.markdown(f"[{sentence}](page?name={params["file_name"]}&keyword={params["keyword"]}&color={params["color"]})", unsafe_allow_html=True)
            #st.page_link("pages/page.py", label = orig[i])
        #st.write("keyword: ", keyword)
    else:
        st.write("Oops! there is nothing found")

# uploaded file
uploaded_file = st.file_uploader("Upload file", type=["txt", "csv", "pdf", "xml", "xlsx"])

if uploaded_file:
    uploadfile(uploaded_file)

key = st.button("show")
if key:
    showlist()