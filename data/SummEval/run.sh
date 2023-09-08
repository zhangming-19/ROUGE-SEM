python calculate_lexical_similarity.py -r reference.txt -c candidate.txt
python calculate_semantic_similarity.py -r reference.txt -c candidate.txt
python candidate_summary_classifier.py -lex_score lexical_similarity.csv -sem_score semantic_similarity.csv
python categorized_summary_rewriter.py -category categorized_summary.csv -c candidate.txt
python rewritten_summary_scorer.py -r reference.txt -c new_candidate.csv