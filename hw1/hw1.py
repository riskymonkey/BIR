import xml.etree.ElementTree as et
import os
import re
import shutil

def searchtitle(keyword, color):
    result = []
    file_name = []
    orig = []
    path = '/bir/pubmed/tumor/xml'
    lower_keyword = keyword.lower()

    for file in os.listdir(path):
        # read xml
        file_path = os.path.join(path, file)
        tree = et.parse(file_path)

        # get articletitle
        root = tree.getroot()
        title = root.find(".//ArticleTitle").text
        lower_title = title.lower()
        lower_title = lower_title.replace('-', ' ')

        # remove punctuation
        rmv = re.sub(r'[^\w\s]', '', lower_title)
        # print(rmv)

        if lower_keyword in rmv:
            highlight = re.sub(f"{keyword}", 
                               lambda m: f'<span style="color:{color}">{m.group(0)}</span>', 
                               title, 
                               flags = re.IGNORECASE)

            result.append(highlight)
            file_name.append(file)
            orig.append(title)

    return result, file_name, orig

def extractcontent(file_name):
    path = '/bir/pubmed/tumor/xml'
    file_path = os.path.join(path, file_name)
    tree = et.parse(file_path)
    root = tree.getroot()
    title = root.find(".//ArticleTitle").text
    journal = root.find(".//Title").text
    abstracts = root.findall(".//AbstractText")

    return title, journal, abstracts

def statistic(content):
    abbreviations = r'\b(?:\d+\.\d+|e\.g\.|i\.e\.|vs\.|etc\.|\w\.\d)'
    modified_content = re.sub(abbreviations, lambda x: x.group(0).replace('.', '<DOT>'), content)
    #print(modified_content)
    sentences = re.split(r'[.!?]+', modified_content)
    #print(sentences)
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

