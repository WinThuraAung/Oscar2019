from myanmartools import ZawgyiDetector
from datasets import load_dataset
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import re


dataset = load_dataset("json", data_files="/Users/macbookpro/Desktop/BaseInternship/oscar-2019-my-fix.json", split="train")

regex_pattern = "(?:(?<!\\u1039)([\\u1000-\\u102A\\u103F\\u104A-\\u104F]|[\\u1040-\\u1049]+|[^\\u1000-\\u104F]+)(?![\\u103E\\u103B]?[\\u1039\\u103A\\u1037]))";


def syllables(text):
    """
    Translated from Java to Python from ReSegment.java
    Breaks sentence down into list of syllables
    """
    if text is None:
        raise ValueError("Input text cannot be None")
    
    # if text is detector.get_zawgyi_probability():
    #     ##convert text into unicode
    #     print()

    RESEGMENT_REGULAR_EX = regex_pattern  
    outputs = re.sub(RESEGMENT_REGULAR_EX, "\U0001D54A\\1", text).split("\U0001D54A")
    
    segment_list = list(outputs)
    
    if len(segment_list) > 0:
        segment_list.pop(0)
    
    return segment_list


def count_syllables(list_syllables):
    return len(syllables(list_syllables))



num_docs = len(dataset)
total_words = 0
total_syllables_with_space = 0
total_syllables_without_space = 0
dataset_size = 0
avg_length_of_docs = 0
total_length = 0
all_words = []
doc_lengths = []
count = 1

for doc in dataset:
    print(count)
    count += 1
    text = doc['text']
    words = text.split()

    total_words += len(words)
    total_length += len(text)

    all_words.extend(words)
    doc_lengths.append(len(text))

    syllables_with_space = count_syllables(text)
    total_syllables_with_space += syllables_with_space 

    syllables_without_space = count_syllables(text.replace(" ", ""))
    total_syllables_without_space += syllables_without_space

    dataset_size += len(doc['text'].encode('utf-8'))


avg_length_of_docs = total_length / num_docs


print(f"Number of documents: {num_docs}")
print(f"Total words: {total_words}")
print(f"Total syllables (with spaces): {total_syllables_with_space}")
print(f"Total syllables (without spaces): {total_syllables_without_space}")
print(f"Dataset size (in bytes): {dataset_size}")
print(f"Average length of documents: {avg_length_of_docs:.2f}")


# Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=30).generate(' '.join(all_words))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Most Frequent Words')
plt.show()

# Visualization: Frequency Histogram
plt.figure(figsize=(10, 5))
sns.histplot(doc_lengths, bins=1000, kde=False)
plt.xscale('log')
plt.xlabel('Document Length')
plt.ylabel('Frequency')
plt.title('Frequency Histogram of Document Lengths')
plt.xlim(0, 15000)
plt.show()

