import sys
import os
import rouge
import bert_score
import argparse
import codecs
import nltk
nltk.download('punkt')
import numpy as np
import pandas as pd


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass


def prepare_results(metric, p, r, f):
    return '\t{}:\t {:5.2f}\t {:5.2f}\t {:5.2f}'.format(metric, 100.0 * p, 100.0 * r,
                                                                 100.0 * f)


def test_rouge(candidates, references):
    candidates = [line.strip() for line in candidates]
    references = [line.strip() for line in references]
    assert len(candidates) == len(references)

    apply_avg = True
    apply_best = False

    evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l', 'rouge-w'],
                            max_n=4,
                            limit_length=True,
                            length_limit=100,
                            length_limit_type='words',
                            apply_avg=apply_avg,
                            apply_best=apply_best,
                            alpha=0.5,  # Default F1_score
                            weight_factor=1.2,
                            stemming=True)

    all_hypothesis = candidates
    all_references = references

    scores = evaluator.get_scores(all_hypothesis, all_references)
#    print(scores)

    rougel = ""
    for metric, results in sorted(scores.items(), key=lambda x: x[0]):
        if metric in ["rouge-1", "rouge-2", "rouge-l"]:
    #        print(prepare_results(metric, results['p'], results['r'], results['f']))
            rougel = rougel + '{:5.2f}'.format(100 * results['f']) + "-"

    print("ROUGE 1-2-L F:", rougel)
    return rougel



def get_sents_str(file_path):
    sents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.lower()
            sents.append(line)
    return sents


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default="candidate.txt",
                        help='candidate file')
    parser.add_argument('-r', type=str, default="reference.txt",
                        help='reference file')
    args = parser.parse_args()

    references = get_sents_str(args.r)
    candidates = get_sents_str(args.c)

    #print(references)
    sys.stdout = Logger('test_log.txt')
    
    print('################### Total #################')
    print('Rouge')
    score_total = test_rouge(candidates, references)
    
    print('################### Each #################')
    R1_list = []
    R2_list = []
    RL_list = []

    for item_c, item_r in zip(candidates, references):
        # 01 Rouge score
        score_tmp = test_rouge(item_c.split('\n'), item_r.split('\n'))
        R1_list.append(score_tmp.split('-')[0])
        R2_list.append(score_tmp.split('-')[1])
        RL_list.append(score_tmp.split('-')[2])
    
    lex_score_list = []
    for item_R1, item_R2, item_RL in zip(R1_list, R2_list, RL_list):
        lex_score_temp = 0.3*item_R1 + 0.3*item_R2 + 0.4*item_RL
        lex_score_list.append(lex_score_temp)

    # Rouge + Bert 
    name = ['ref', 'can', 'R1', 'R2', 'RL', 'lex_score']
    temp = []
    temp.append(references)
    temp.append(candidates)
    temp.append(R1_list)
    temp.append(R2_list)
    temp.append(RL_list)
    temp.append(lex_score_list)
    temp_df = np.array(temp)
    temp_df = temp_df.T
    temp_df = pd.DataFrame(temp_df, columns=name)
    temp_df.to_csv('lexical_similarity.csv', encoding='utf-8')




