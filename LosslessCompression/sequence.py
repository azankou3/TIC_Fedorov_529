import random
import collections
import math
import string
import matplotlib.pyplot as plt
open("results_sequence.txt", "w")

variant = 14
list1 = [1] * variant
list0 = [0] * (100-variant)

list_100 = list1 + list0
random.shuffle(list_100)
sequence1 = "".join((map(str, list_100)))

list_1 = ["f", "e", "d", "o", "r", "o", "v"]
list_0 = [0] * (100 - len(list_1))
list_01 = list_1 + list_0
sequence2 = "".join(map(str, list_01))
random.shuffle(list_01)
sequence3 = "".join(map(str, list_01))
print(sequence2)
print(sequence3)

sequence4 = ["f", "e", "d", "o", "r", "o", "v", "5", "2", "9"] * 10
sequence4 = "".join(map(str, sequence4))
print(sequence4)
sequence5 = ["f", "e", "5", "2", "9"] * 20
random.shuffle(sequence5)
sequence5 = "".join(map(str, sequence5))
print(sequence5)

name = ["f", "e"] * 35
number = ["5", "2", "9"] * 10
sequence6 = name + number
random.shuffle(sequence6)
sequence6 = "".join(map(str, sequence6))
print(sequence6)


elements = string.ascii_lowercase + string.digits
list_100 = [random.choice(elements) for _ in range(100)]
sequence7 = "".join(map(str, list_100))
print(sequence7)

sequence8 = [1] * 100
sequence8 = "".join(map(str, sequence8))
print(sequence8)

original_sequences = [sequence1, sequence2, sequence3, sequence4,
                          sequence5, sequence6, sequence7, sequence8]


with open("sequence.txt", "w") as file:
    print(original_sequences, file=file)

Original_sequence_size = 800
results = []
for sequence in original_sequences:
    counts = collections.Counter(sequence)
    unique_chars = set(sequence)
    sequence_alphabet_size = len(unique_chars)

    probability = {symbol: count / 100 for symbol, count in counts.items()}

    probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])

    mean_probability = sum(probability.values()) / len(probability)
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in
                probability.values())
    if equal:
        uniformity = "uniformity"
    else:
        uniformity = "non uniformity"
    entropy = -sum(p * math.log2(p) for p in probability.values())

    if sequence_alphabet_size > 1:
        source_excess = 1 - entropy / math.log2(sequence_alphabet_size)
    else:
        source_excess = 1
    results.append([sequence_alphabet_size, round((entropy), 2),
                    round((source_excess), 2), uniformity])
    with open("results_sequence.txt", "a") as file:
        print(f"Sequence: {sequence} \n "
            f"Length sequence: {len(sequence)} byte \n "
            f"Length alphabet: {sequence_alphabet_size} \n "
            f"Probability symbols: {probability_str} \n"
            f"Mean probability: {mean_probability:.2f} \n "
            f"Symbol count: {uniformity} \n "
            f"Entropy:  {entropy:.4f} \n "
            f"Source excess: {source_excess:.2f} \n \n", file=file)

fig, ax = plt.subplots(figsize=(14/1.54, 14/1.54))
headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4',
       'Послідовність 5', 'Послідовність 6','Послідовність 7', 'Послідовність 8']
ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=row,
loc='center' , cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
plt.savefig("Характеристики сформованих послідовностей", dpi=600)
