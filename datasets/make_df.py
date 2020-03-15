import pandas as pd

with open('handpicked_words.txt', 'r') as f:
    words = f.read().splitlines()
    # print(words)

with open('filtered_fillers', 'r') as f:
    fillers = f.read().splitlines()
    # print(fillers)

dic = {}

for w in words:
    dic.update({w: 1.0})

for w in fillers:
    dic.update({w: 0.0})

df = pd.DataFrame(dic.items(), columns=['WORD', 'GROUND_TRUTH'])
print(df.head())
df.to_csv('dataset_1.csv', index=False)
