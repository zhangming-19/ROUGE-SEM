#!/bin/bash

echo "Calculate Lexical Similarity"
python calculate_lexical_similarity.py -r reference.txt -c candidate.txt

echo "Calculate Semantic Similarity"
python calculate_semantic_similarity.py -r reference.txt -c candidate.txt

echo "Candidate Summary Classifier"
python candidate_summary_classifier.py -lex_score lexical_similarity.csv -sem_score semantic_similarity.csv

echo "Categorized Summary Rewriter"
python categorized_summary_rewriter.py -category categorized_summary.csv -c candidate.txt

echo "Rewritten Summary Scorer"
python rewritten_summary_scorer.py -r reference.txt -c new_candidate.csv