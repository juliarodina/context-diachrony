**ELMo models for diachronic research:**  

**Code to train ELMo models:** https://github.com/ltgoslo/simple_elmo_training

**Code to get ELMo embeddings from models:** https://github.com/ltgoslo/simple_elmo  


**Datasets:** https://github.com/juliarodina/context-diachrony/tree/master/datasets  
- dataset_0: target words changed from the pre-Soviet times through the Soviet times, from work "Two centuries in two thousand words: Neural embedding models in detecting diachronic lexical changes" [Kutuzov & Kuzmenko, 2018], fillers were re-generated and randomly downsampled to 28 fillers. 43+28=71 words in all.
- dataset_1: 42 words changed from the Soviet times through the post-Soviet times: 35 nouns and 7 adjectives. Handpicked from "Новые слова и значения" ИЛИ РАН, "Толковый словарь русского языка конца ХХ века" Скляревской. 1 filler for each word from the same frequency percentile, then randomly downsampled to 27 fillers. 69 words in all.  

**Annotation methodology:** _Diachronic Usage Relatedness (DURel): A Framework for the Annotation of Lexical Semantic Change_ [Schlechtweg et al., 2018] https://www.aclweb.org/anthology/N18-2027/  

- dataset\_n\_annotation.tsv: pairs of context sentences for words from datasets, annotated by 5 people
- dataset\_n\_testest.tsv: aggregated annotations with mean values for each group (_earlier, compare, later_), Δlater value, frequencies in each corpus
- dataset\_n\_testest_filtered.tsv: same aggregated annotations, filtered by Krippendorff's alpha value > 0.2

**Experiments:** https://github.com/juliarodina/context-diachrony/tree/master/code/evaluation  

For three types of models:
- models trained on all corpora from all time periods, differentiation is made at the inference stage;
- models trained incrementally on each corpora successively;
- models tranied on corpora from each time period separately.
