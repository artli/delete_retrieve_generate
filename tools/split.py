import sys

from ..utils import generate_tokens, generate_preprocessed_sentences, split_sentence


def split_corpus(corpus_file, vocab: set, attribute_vocab: set):
    with open(corpus_file + '.content', 'w', encoding='utf-8') as content_output, \
         open(corpus_file + '.attributes', 'w', encoding='utf-8') as attribute_output:
        for sentence in generate_preprocessed_sentences(corpus_file, vocab):
            content, attributes = split_sentence(sentence, attribute_vocab)
            content_output.write(' '.join(content) + '\n')
            attribute_output.write(' '.join(attributes) + '\n')


def main():
    vocab_file, attribute_file, *corpus_files = sys.argv[1:]

    vocab = set(generate_tokens(vocab_file))
    attribute_vocab = set(generate_tokens(attribute_file))
    for corpus_file in corpus_files:
        split_corpus(corpus_file, vocab, attribute_vocab)


if __name__ == '__main__':
    main()
