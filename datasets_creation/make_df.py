import pandas as pd
import random

with open('words_1.txt', 'r') as f:
    words = f.read().splitlines()
    # print(words)

with open('fillers_1.txt', 'r') as f:
    fillers = f.read().splitlines()
    # print(fillers)
fillers = random.sample(fillers, 27)
print(fillers)
dic = {}

for w in words:
    dic.update({w: 1.0})

for w in fillers:
    dic.update({w: 0.0})

df = pd.DataFrame(dic.items(), columns=['WORD', 'GROUND_TRUTH'])
print(df.head())
df.to_csv('dataset_1.csv', index=False)
