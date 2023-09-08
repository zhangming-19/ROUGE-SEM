# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 20:53:19 2023

@author: zhangming
"""
import os
import torch
import argparse
from scipy.spatial.distance import cosine
from transformers import AutoModel, AutoTokenizer
import pandas as pd
import tqdm
import csv

Alpha_parameter = 0.5
Beta_parameter = 0.5

parser = argparse.ArgumentParser()
parser.add_argument('-lex_score', type=str, default="lexical_similarity.csv",
                    help='candidate file')
parser.add_argument('-sem_score', type=str, default="semantic_similarity.csv",
                    help='reference file')
args = parser.parse_args()

lex_df = pd.read_csv(args.lex_score)
lex_score_list = lex_df["lex_score"].tolist()
references = lex_df["ref"].tolist()
candidates = lex_df["can"].tolist()

sem_df = pd.read_csv(args.sem_score)
sem_score_list = sem_df["sem_score"].tolist()    

category_list = []
for item_lex, item_sem in zip(lex_score_list, sem_score_list):
    if item_lex >= Alpha_parameter and item_sem >= Beta_parameter:
        category_list.append(0)
    if item_lex >= Alpha_parameter and item_sem < Beta_parameter:
        category_list.append(1)
    if item_lex < Alpha_parameter and item_sem >= Beta_parameter:
        category_list.append(2)
    if item_lex < Alpha_parameter and item_sem < Beta_parameter:
        category_list.append(3)

name = ['ref', 'can', 'lex_score', 'sem_score', 'category']
temp = []
temp.append(references)
temp.append(candidates)
temp.append(lex_score_list)
temp.append(sem_score_list)
temp.append(category_list)
temp_df = np.array(temp)
temp_df = temp_df.T
temp_df = pd.DataFrame(temp_df, columns=name)
temp_df.to_csv('categorized_summary.csv', encoding='utf-8')
            
