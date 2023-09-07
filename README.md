# ROUGE-SEM: Better evaluation of summarization using ROUGE combined with semantics

This project includes the source code for the paper [**ROUGE-SEM: Better evaluation of summarization using ROUGE combined with semantics**](https://www.sciencedirect.com/science/article/pii/S0957417423018663), appearing at Expert Systems with Applications. Please cite this [article](https://www.sciencedirect.com/science/article/pii/S0957417423018663) as follows, if you use this code.
M. Zhang, C. Li, M. Wan et al., ROUGE-SEM: Better evaluation of summarization using ROUGE combined with semantics. Expert Systems With Applications (2023), doi: https://doi.org/10.1016/j.eswa.2023.121364.

**Highlighted Features**

* A framework of ROUGE combined with semantics is proposed for summarization evaluation.
* A classification of Summary based on semantic and lexical similarity to the reference.
* Variants of ROUGE-SEM outperform the corresponding variants of ROUGE consistently.

> Stock movement prediction is a challenging problem: the market is highly *stochastic*, and we make *long-term* predictions from *chaotic* data. We treat these three complexities and present a novel long-term stock movement prediction approach based on research reports. In detail, a new Research Report dataset for Stock Movement Prediction (SMPRR) is proposed. SMPRR is one of the few datasets for long-term stock movement prediction, which is mainly composed of long-form, formal, and professional research reports. We demonstrate the state-of-the-art performance of our proposed model on SMPRR.

<!--You might also be interested in our code for stock movement prediction. We have deposited the code in the Code Ocean platform. The accepted code capsules can be found through https://codeocean.com/capsule/8892872/tree/v1. The DOI of the code is https://doi.org/10.24433/CO.2855516.v1
-->

Should you have any query please contact me at [zhangming@hccl.ioa.ac.cn](mailto:zhangming@hccl.ioa.ac.cn).

## Codes
### Requirements
We use Conda python 3.7 and strongly recommend that you create a new environment.
* Prerequisite: Python 3.7 or higher versions
```shell script
conda create -n ROUGE-SEM python=3.7
```

### Environment
* Install all packages in requirement.txt.
* Python 3.7
* PyTorch 1.4.0+cu100
* HuggingFace Transformers 4.16.2
* boto3 1.24.32
* numpy 1.21.4
* pandas 1.1.5
* regex 2022.7.9
* sentencepiece 0.1.96
* sklearn latest
```shell script
pip3 install -r requirements.txt
```


### Set Up for ROUGE 
* Read more from the [link](https://github.com/bheinzerling/pyrouge).
```shell script
git clone https://github.com/summanlp/evaluation
export ROUGE_EVAL_HOME="yourPath/evaluation/ROUGE-RELEASE-1.5.5/data/"
pip install pyrouge
pyrouge_set_rouge_path yourPath/evaluation/ROUGE-RELEASE-1.5.5
```




## Example Use Cases

### Evaluate Multi-Document Summaries (*evaluate_summary.py*)
Given the source documents and some to-be-evaluated summaries, you can produce the unsupervised metrics for the summaries with the code below:

```python
from ref_free_metrics.supert import Supert
from utils.data_reader import CorpusReader

# read docs and summaries
reader = CorpusReader('data/topic_1')
source_docs = reader()
summaries = reader.readSummaries() 

# compute the Supert scores
supert = Supert(source_docs, ref_metric='top15') 
scores = supert(summaries)
```
In the example above, it extracts the top-15 sentences from each source document
to build the *pseudo reference summaries*, and rate the summaries
by measuring their semantic similarity with the pseudo references.

### Evaluate Single-Document Summaries 
You could use the same code for evaluating multi-doc summaries to rate single-doc summaries.
In addition to that, you may consider using more sentences from the input doc to 
build the pseudo reference, by replacing argument 'top15' in the above code by, e.g., 'top30',
so as to use the first 30 (instead of 15) sentences to build the pseudo reference.

We study the influence of pseudo reference length on the performance of Supert 
for single-doc summaries at [summ_eval](summ_eval/). We compare
correlation between Supert and human ratings from the [SummEval](https://github.com/Yale-LILY/SummEval)
dataset.


## Citation
@article{ZHANG2023121364,
title = {ROUGE-SEM: Better evaluation of summarization using ROUGE combined with semantics},
journal = {Expert Systems with Applications},
pages = {121364},
year = {2023},
issn = {0957-4174},
doi = {https://doi.org/10.1016/j.eswa.2023.121364},
url = {https://www.sciencedirect.com/science/article/pii/S0957417423018663},
author = {Ming Zhang and Chengzhang Li and Meilin Wan and Xuejun Zhang and Qingwei Zhao},
keywords = {Automatic summarization evaluation, Semantic similarity, Lexical similarity, Contrastive learning, Back-translation},
abstract = {With the development of pre-trained language models and large-scale datasets, automatic text summarization has attracted much attention from the community of natural language processing, but the progress of automatic summarization evaluation has stagnated. Although there have been efforts to improve automatic summarization evaluation, ROUGE has remained one of the most popular metrics for nearly 20 years due to its competitive evaluation performance. However, ROUGE is not perfect, there are studies have shown that it is suffering from inaccurate evaluation of abstractive summarization and limited diversity of generated summaries, both caused by lexical bias. To avoid the bias of lexical similarity, more and more meaningful embedding-based metrics have been proposed to evaluate summaries by measuring semantic similarity. Due to the challenge of accurately measuring semantic similarity, none of them can fully replace ROUGE as the default automatic evaluation toolkit for text summarization. To address the aforementioned problems, we propose a compromise evaluation framework (ROUGE-SEM) for improving ROUGE with semantic information, which compensates for the lack of semantic awareness through a semantic similarity module. According to the differences in semantic similarity and lexical similarity, summaries are classified into four categories for the first time, including good-summary, pearl-summary, glass-summary, and bad-summary. In particular, the back-translation technique is adopted to rewrite pearl-summary and glass-summary that are inaccurately evaluated by ROUGE to alleviate lexical bias. Through this pipeline framework, summaries are first classified by candidate summary classifier, then rewritten by categorized summary rewriter, and finally scored by rewritten summary scorer, which are efficiently evaluated in a manner consistent with human behavior. When measured using Pearson, Spearman, and Kendall rank coefficients, our proposal achieves comparable or higher correlations with human judgments than several state-of-the-art automatic summarization evaluation metrics in dimensions of coherence, consistency, fluency, and relevance. This also suggests that improving ROUGE with semantics is a promising direction for automatic summarization evaluation.}
}
