# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:22:41 2021

@author: zhangming
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt
import time
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

option = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=option)
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

def get_url_En2Cn(text:str):
    url_part1 = 'https://translate.google.com/?hl=zh-CN&sl=en&tl=zh-CN&text='
    url_part2 = text
    url_part3 = '&op=translate'
    GOOGLE_TRANSLATE_URL = url_part1 + url_part2 + url_part3
    return GOOGLE_TRANSLATE_URL

def get_url_Cn2En(text:str):
    url_part1 = 'https://translate.google.com.hk/?sl=zh-CN&tl=en&text='
    url_part2 = text
    url_part3 = '&op=translate'
    GOOGLE_TRANSLATE_URL = url_part1 + url_part2 + url_part3
    return GOOGLE_TRANSLATE_URL

def get_url_En2Fr(text:str):
    url_part1 = 'https://translate.google.com.hk/?sl=en&tl=fr&text='
    url_part2 = text
    url_part3 = '&op=translate'
    GOOGLE_TRANSLATE_URL = url_part1 + url_part2 + url_part3
    return GOOGLE_TRANSLATE_URL

def get_url_Fr2En(text:str):
    url_part1 = 'https://translate.google.com.hk/?sl=fr&tl=en&text='
    url_part2 = text
    url_part3 = '&op=translate'
    GOOGLE_TRANSLATE_URL = url_part1 + url_part2 + url_part3
    return GOOGLE_TRANSLATE_URL


def translate_En2Cn(input_text):
    try:
        url = get_url_En2Cn(input_text) 
        browser.get(url) 
        time.sleep(3)
        trans = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        "#yDmH0d > c-wiz > div > div.WFnNle > c-wiz > div.OlSOob > c-wiz > div.ccvoYb.EjH7wc > div.AxqVh > div.OPPzxe > c-wiz.mxfMQ > div > div.usGWQd > div > div.lRu31")))
        output_text = trans.text.replace('\n', '')
        print('*'*10)
        print(output_text)
        time.sleep(2)
        return output_text
    except:
        print('@'*10)
        print('translate error!')
        return input_text
    
def translate_Cn2En(input_text):
    try:
        url = get_url_Cn2En(input_text) 
        browser.get(url) 
        time.sleep(3)
        trans = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        "#yDmH0d > c-wiz > div > div.WFnNle > c-wiz > div.OlSOob > c-wiz > div.ccvoYb.EjH7wc > div.AxqVh > div.OPPzxe > c-wiz.mxfMQ > div > div.usGWQd > div > div.lRu31")))
        output_text = trans.text.replace('\n', '')
        print('*'*10)
        print(output_text)
        time.sleep(2)
        return output_text
    except:
        print('@'*10)
        print('translate error!')
        return input_text

def translate_En2Fr(input_text):
    try:
        url = get_url_En2Fr(input_text) 
        browser.get(url) 
        time.sleep(3)
        trans = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        "#yDmH0d > c-wiz > div > div.WFnNle > c-wiz > div.OlSOob > c-wiz > div.ccvoYb.EjH7wc > div.AxqVh > div.OPPzxe > c-wiz.mxfMQ > div > div.usGWQd > div > div.lRu31")))
        output_text = trans.text.replace('\n', '')
        print('*'*10)
        print(output_text)
        time.sleep(2)
        return output_text
    except:
        print('@'*10)
        print('translate error!')
        return input_text

def translate_Fr2En(input_text):
    try:
        url = get_url_Fr2En(input_text) 
        browser.get(url) 
        time.sleep(3)
        trans = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        "#yDmH0d > c-wiz > div > div.WFnNle > c-wiz > div.OlSOob > c-wiz > div.ccvoYb.EjH7wc > div.AxqVh > div.OPPzxe > c-wiz.mxfMQ > div > div.usGWQd > div > div.lRu31")))
        output_text = trans.text.replace('\n', '')
        print('*'*10)
        print(output_text)
        time.sleep(2)
        return output_text
    except:
        print('@'*10)
        print('translate error!')
        return input_text

def get_sents_str(file_path):
    sents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.lower()
            sents.append(line)
    return sents

# read data
parser = argparse.ArgumentParser()
parser.add_argument('-category', type=str, default="categorized_summary.csv",
                    help='candidate file')
parser.add_argument('-c', type=str, default="candidate.txt",
                    help='reference file')
args = parser.parse_args()

cate_df = pd.read_csv(args.category)
cate_list = cate_df["category"].tolist()
can_list = get_sents_str(args.c)

new_sum_Cn_list = []
new_sum_En_list = []
for item_cate, item_can in zip(cate_list, can_list):
    if item_cate == 1 or item_cate == 2:
        input_text = item_can
        translate_text = translate_En2Fr(input_text)    
        new_sum_Cn_list.append(translate_text)
        input_text = translate_text.replace('\n', '')
        translate_text = translate_Fr2En(input_text)
        new_sum_En_list.append(translate_text)    
    else:
        new_sum_En_list.append(item_can)

    
# save data
name = ['can', 'category', 'sum-Cn', 'new_can']
temp = []
temp.append(can_list)
temp.append(cate_list)
temp.append(new_sum_Cn_list)
temp.append(new_sum_En_list)
temp_df = np.array(temp)
temp_df = temp_df.T
temp_df = pd.DataFrame(temp_df, columns=name)
temp_df.to_csv('new_candidate.csv', encoding='utf-8', index=None)

browser.close()


