import itertools


UNKNOWN = '<unk>'


def nested_iter(d):
    for k, v in sorted(d.items()):
        if isinstance(v, dict):
            for ki, vi in nested_iter(v):
                yield k + '|' + ki, vi
        else:
            yield k, v


def config_val_string(config):
    config_items = [kv for kv in nested_iter(config)]
    config_vals = map(lambda x: str(x[1]), config_items)
    return ','.join(config_vals)


def config_key_string(config):
    config_items = [kv for kv in nested_iter(config)]
    config_keys = map(lambda x: str(x[0]), config_items)
    return ','.join(config_keys)


def generate_sentences(filename):
    with open(filename, encoding='utf-8') as f:
        yield from map(str.split, f)


def generate_tokens(filename):
    yield from itertools.chain.from_iterable(generate_sentences(filename))


def read_sentences(filename):
    return list(generate_sentences(filename))


def read_tokens(filename):
    return list(generate_tokens(filename))


def preprocess_sentence(sent, vocab: set, unknown=UNKNOWN):
    return [
        token if token in vocab else unknown
        for token in sent]


def preprocess_sentences(sentences, vocab: set, unknown=UNKNOWN):
    for sent in sentences:
        yield preprocess_sentence(sent, vocab, unknown=unknown)


def generate_preprocessed_sentences(filename, vocab: set):
    return preprocess_sentences(generate_sentences(filename), vocab)


def read_corpus(filename, vocab: set):
    return list(generate_preprocessed_sentences(filename, vocab))


def split_sentence(sentence, attribute_vocab: set):
    content = []
    attributes = []
    for token in sentence:
        if token in attribute_vocab:
            attributes.append(token)
        else:
            content.append(token)
    return content, attributes
