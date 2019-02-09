"""
args:
1 corpus file (tokenized)
2 K
prints K most frequent vocab items
"""

import sys
from collections import Counter
from itertools import chain
from operator import itemgetter

from ..utils import generate_tokens


FIRST_TOKENS = ['<unk>', '<pad>', '<s>', '</s>']


def get_all_tokens(filenames, cutoff):
    counter = Counter(chain(FIRST_TOKENS, *map(generate_tokens, filenames)))
    return list(map(itemgetter(0), counter.most_common(cutoff)))


def main():
    cutoff, *filenames = sys.argv[1:]
    cutoff = int(cutoff)
    print('\n'.join(get_all_tokens(filenames, cutoff)))


if __name__ == '__main__':
    main()
