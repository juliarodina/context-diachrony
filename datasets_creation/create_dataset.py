import pandas as pd
import gensim
from scipy.stats import percentileofscore
import random
import numpy as np

with open('words_0.txt', 'r') as f:
    words = f.read().splitlines()

print('gold dataset length: ', len(words))
dic = {}

emb_model_0 = gensim.models.KeyedVectors.load_word2vec_format('../macro/models_static/pre-soviet.bin.gz',
                                                            binary=True, unicode_errors='replace')
print('model 1 loaded')
emb_model_1 = gensim.models.KeyedVectors.load_word2vec_format('../macro/models_static/soviet.bin.gz',
                                                            binary=True, unicode_errors='replace')
print('model 2 loaded')

vocab_0 = emb_model_0.vocab
vocab_1 = emb_model_1.vocab
vocablist = [vocab_0, vocab_1]

corpus_size = [59579878, 54299964]


def get_freqdict(wordlist, vocablist, corpus_size, return_percentiles=True):
    all_freqs = []
    word_freq = {}
    for word in wordlist:
        # print(word)
        counts = [vocab[word].count for vocab in vocablist]
        # print(counts)
        frequency = [counts[i] / corpus_size[i] for i in range(len(vocablist))]
        mean_frequency = sum(frequency) / len(frequency)
        # print(mean_frequency)
        word_freq[word] = mean_frequency
        # print('='*80)

    intersec = set.intersection(*map(set, vocablist))
    for word in intersec:
        counts = [vocab[word].count for vocab in vocablist]
        frequency = [counts[i] / corpus_size[i] for i in range(len(vocablist))]
        mean_frequency = sum(frequency) / len(frequency)
        all_freqs.append(mean_frequency)
    # print(all_freqs)
    # print(word_freq)

    if return_percentiles:
        percentiles = {}
        for word in wordlist:
            percentiles[word] = int(percentileofscore(all_freqs, word_freq[word]))
            # print(word, 'freq--- ', word_freq[word], 'perc--- ', percentiles[word])
        return percentiles

    else:
        return word_freq


def output_results(evaluative_dict, rest_dict):
    rest_dict_inv = {}

    for key, value in rest_dict.items():
        rest_dict_inv.setdefault(value, []).append(key)

    finallist = set()
    missing_perc = []

    for i in evaluative_dict:
        print('target: ', i)
        perc = evaluative_dict[i]
        print(perc)
        try:
            sl = random.sample(rest_dict_inv[perc], 4)
        except (ValueError, KeyError):
            missing_perc.append(evaluative_dict[i])
            continue
        for l in sl:
            print(l)
            finallist.add(l)
            rest_dict_inv[perc].remove(l)
        print('='*30)

    return list(finallist)


def delete_lowfrequent(wordlist, threshold, vocablist):
    newlist = set()
    for word in wordlist:
        hit = False
        for vocab in vocablist:
            if vocab[word].count < threshold:
                hit = True
                break
        if hit:
            continue
        newlist.add(word)

    return newlist


intersec = set.intersection(*map(set, vocablist))

nouns = []
adjs = []
for word in words:
    if word.split('_')[-1] == 'NOUN':
        nouns.append(word)
    elif word.split('_')[-1] == 'ADJ':
        adjs.append(word)

print('Generating fillers...')
wordfreq_nouns = get_freqdict(nouns, vocablist, corpus_size)
wordfreq_adjs = get_freqdict(adjs, vocablist, corpus_size)
# print(wordfreq_nouns, (), wordfreq_adjs)

filler_noun = set()
filler_adj = set()
for voc_word in intersec:
    if voc_word.endswith('NOUN') and voc_word not in words:
        filler_noun.add(voc_word)
    elif voc_word.endswith('ADJ') and voc_word not in words:
        filler_adj.add(voc_word)

filler_noun = delete_lowfrequent(filler_noun, 0, vocablist)
filler_adj = delete_lowfrequent(filler_adj, 0, vocablist)

fillerfreq_noun = get_freqdict(filler_noun, vocablist, corpus_size)
fillerfreq_adj = get_freqdict(filler_adj, vocablist, corpus_size)
# print(fillerfreq_noun, (), fillerfreq_adj)

res_nouns = output_results(wordfreq_nouns, fillerfreq_noun)
res_adj = output_results(wordfreq_adjs, fillerfreq_adj)

print('n fillers: ', len(res_adj)+len(res_nouns))
print('ADJ: \n', len(res_adj), res_adj)
print('NOUN: \n', len(res_nouns), res_nouns)