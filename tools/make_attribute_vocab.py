"""
python make_attribute_vocab.py [vocab] [corpus1] [corpus2] r

subsets a [vocab] file by finding the words most associated with 
one of two corpuses. threshold is r ( # in corpus_a  / # in corpus_b )
"""

import sys
import itertools
from collections import Counter

from ..utils import generate_tokens, read_corpus


class SalienceCalculator(object):
    def __init__(self, flattened_corpuses):
        self.counters = list(map(Counter, flattened_corpuses))

    def saliences(self, token, lambda_=0.5):
        counts = [counter[token] for counter in self.counters]
        count_sum = sum(counts)
        return [(count + lambda_) / (count_sum - count + lambda_) for count in counts]


def main():
    vocab_file, *corpus_descriptions = sys.argv[1:]

    corpus_files = corpus_descriptions[0::3]
    attribute_files = corpus_descriptions[1::3]
    min_saliences = list(map(float, corpus_descriptions[2::3]))

    vocab = set(generate_tokens(vocab_file))
    flattened_corpuses = [
        list(itertools.chain.from_iterable(read_corpus(filename, vocab)))
        for filename in corpus_files]
    calculator = SalienceCalculator(flattened_corpuses)

    attribute_lists = [[] for _ in attribute_files]
    for token in vocab:
        saliences = calculator.saliences(token)
        for salience, attribute_list, min_salience in zip(saliences, attribute_lists, min_saliences):
            if salience > min_salience:
                attribute_list.append(token)

    for attribute_list, attribute_file in zip(attribute_lists, attribute_files):
        with open(attribute_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(attribute_list))


if __name__ == '__main__':
    main()
