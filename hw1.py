import xml.etree.ElementTree as et
import streamlit as st
import os
import re
import shutil

def searchtitle(keyword, color, mode):
    result = []
    file_name = []
    orig = []
    count = []
    path = '/bir/pubmed/tumor/xml'
    lower_keyword = keyword.lower()

    for file in os.listdir(path):
        tmp = file.split(".")
        if tmp[1] == "xml":
            # read xml
            file_path = os.path.join(path, file)
            tree = et.parse(file_path)

            # get articletitle
            root = tree.getroot()
            title = root.find(".//ArticleTitle").text
            pmid = root.find(".//PMID").text
            lower_title = title.lower()
            lower_title = lower_title.replace('-', ' ')

            if mode == "Default":
                # get articleabstract
                _, _, abstracts, _, _ = extractcontent(file)

                # remove punctuation
                rmv = re.sub(r'[^\w\s]', '', lower_title)

                if lower_keyword in rmv:
                    tmp_count = rmv.lower().count(lower_keyword)
                    highlight = re.sub(f"{keyword}", 
                                    lambda m: f'<span style="color:{color}">{m.group(0)}</span>', 
                                    title, 
                                    flags = re.IGNORECASE)

                    result.append(title)
                    file_name.append(file)
                    continue
                    #file_name.append(file)
                    #orig.append(title)
                    #count.append(tmp_count)
                for abstract in abstracts:
                    content = ''.join(abstract.itertext())
                    lower_content = content.lower()
                    if lower_keyword in lower_content:
                        result.append(title)
                        file_name.append(file)
                        break
            else:
                if keyword in pmid:
                    result.append(title)
                    file_name.append(file)

    #return result, file_name, orig, count
    return result, file_name

def extractcontent(file_name):
    path = '/bir/pubmed/tumor/xml'
    file_path = os.path.join(path, file_name)
    tree = et.parse(file_path)
    root = tree.getroot()
    title = root.find(".//ArticleTitle").text
    journal = root.find(".//Title").text
    abstracts = root.findall(".//AbstractText")
    pmid = root.find(".//PMID").text

    full_name = []
    for author in root.findall(".//Author"):
        last_name = author.find("LastName").text
        fore_name = author.find("ForeName").text
        #affiliation = author.find(".//Affiliation").text
        #print(f"Author: {fore_name} {last_name}, Affiliation: {affiliation}")
        tmp = last_name + " " + fore_name
        full_name.append(tmp)

    return title, journal, abstracts, pmid, full_name

def statistic(content):
    abbreviations = r'\b(?:\d+\.\d+|e\.g\.|i\.e\.|vs\.|etc\.|\w\.\d)'
    modified_content = re.sub(abbreviations, lambda x: x.group(0).replace('.', '<DOT>'), content)
    
    sentences = re.split(r'[.!?]+', modified_content)
    
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_cnt = len(sentences)

    #words = re.findall(r'\b[a-zA-Z]+\b', content)
    words = content.split()
    word_cnt = len(words)

    #letters = re.findall(r'[a-zA-Z]', content)
    letter_cnt = len(content)

    ascii_cnt = sum(1 for char in content if ord(char) < 128)

    return sentence_cnt, word_cnt, letter_cnt, ascii_cnt

def uploadfile(file):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    folder_path = "/bir/pubmed/tumor/xml"
    target = os.path.join(folder_path, file.name)
    tmp_save_path = os.path.join("uploads", file.name)
    with open(tmp_save_path, "wb") as f:
        f.write(file.getbuffer())
    shutil.copy(tmp_save_path, target)

def showlist():
    path = "/bir/pubmed/tumor/xml"
    files = os.listdir(path)

    for file_name in files:
        file_path = os.path.join(path, file_name)
        
        # Parse and display the XML file content
        try:
            tree = et.parse(file_path)
            root = tree.getroot()
            st.write(f"**XML File: {file_name}**")
            # st.write(ET.tostring(root, encoding='unicode'))
        except et.ParseError:
            st.write(f"**Other file: {file_name}**")

def highlight(input_str, keyword, color):
    res = re.sub(f"{keyword}", 
                lambda m: f'<span style="color:{color}">{m.group(0)}</span>', 
                input_str, 
                flags = re.IGNORECASE)
    return res

def file_statistic(file_name, keyword, color):
    _, _, abstracts, pmid, _ = extractcontent(file_name)
    sentence_cnt = 0
    word_cnt = 0
    letter_cnt = 0
    ascii_cnt = 0
    
    highlight_pmid = highlight(pmid, keyword, color)
    st.markdown(f"{highlight_pmid}", unsafe_allow_html=True)
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
    non_ascii = letter_cnt - ascii_cnt
    
    return sentence_cnt, word_cnt, letter_cnt, ascii_cnt, non_ascii
# 提取 PMID
# pmid = root.find(".//PMID").text
# print(f"PMID: {pmid}")

# # 提取作者名單
# for author in root.findall(".//Author"):
#     last_name = author.find("LastName").text
#     fore_name = author.find("ForeName").text
#     affiliation = author.find(".//Affiliation").text
#     print(f"Author: {fore_name} {last_name}, Affiliation: {affiliation}")

# # 提取關鍵詞
# keywords = [kw.text for kw in root.findall(".//Keyword")]
# print(f"Keywords: {', '.join(keywords)}")

