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

def get_sents_str(file_path):
    sents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.lower()
            sents.append(line)
    return sents

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=str, default="candidate.txt",
                    help='candidate file')
parser.add_argument('-r', type=str, default="reference.txt",
                    help='reference file')
args = parser.parse_args()

ref_path = get_sents_str(args.r)
can_path = get_sents_str(args.c)
    
# Import our models. The package will take care of downloading the models automatically
tokenizer = AutoTokenizer.from_pretrained("./model")
model = AutoModel.from_pretrained("./model")

#  read ref
with open(ref_path, 'r', encoding='utf-8') as f:
    ref_summary = f.readlines()
    
# Tokenize input texts
ref_inputs = tokenizer(ref_summary, padding=True, truncation=True, return_tensors="pt")

# Get the embeddings
with torch.no_grad():
    ref_embeddings = model(**ref_inputs, output_hidden_states=True, return_dict=True).pooler_output
    
#  read can
data_list = []
similar_lst = []

with open(can_path, 'r', encoding='utf-8') as f:
    can_summary = f.readlines()
    can_inputs = tokenizer(can_summary, padding=True, truncation=True, return_tensors="pt")
    
with torch.no_grad():
    can_embeddings = model(**can_inputs, output_hidden_states=True, return_dict=True).pooler_output

# Calculate cosine similarities
for i in tqdm.tqdm(range(len(can_embeddings))):
    cosine_sim_ref_can = 1 - cosine(ref_embeddings[i], can_embeddings[i])
    similar_lst.append(cosine_sim_ref_can)
                           
for a,b,c in zip(ref_summary,can_summary,similar_lst):
    x = {}
    x['ref']= a
    x['can']= b
    x['Sem'] = c
    data_list.append(x)

outpath = './semantic_similarity.csv'
with open(outpath, 'w', newline='', encoding='UTF-8') as f_c_csv:
    writer = csv.writer(f_c_csv)
    writer.writerow(['ref', 'can','sem_score'])
    for nl in data_list:
        writer.writerow(nl.values())
            
