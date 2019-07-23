# CUSTOM TOKENIZER FUNCTION

# Custom tokenizer function for text preprocessing.
# The following function does the following:
#   - Lemmatize the sentence
#   - Split it into tokens
#   - Remove common stopwords
#   - Remove punctuation
#   - Keep only letters (no numbers of other symbols)
#   - Remove custom stopwords


# INPUTS:
#   - List of sentences to process (if you have a single one, declare it as a list)


# OUTPUT:
#   - List of sentences processed (containing joined tokens)

import string
import spacy
from tqdm import tqdm_notebook as tqdm


def custom_tokenizer(texts, mode=1):
    # disabling Named Entity Recognition for speed
    nlp = spacy.load('en_core_web_lg', disable=['ner'])
    punctuations = string.punctuation
    # Add custom stopwords
    custom_stop = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                   'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']

    for w in custom_stop:
        nlp.vocab[w].is_stop = True

    # Utility function
    def cleaning(doc, mode):
        # Does cleaning according to mode:
        # mode=1 ---- Lemmatization & stopwords
        # mode=2 ---- Stopwords
        # mode=3 ---- Lemmatization

        if mode == 1:
            txt = [token.lemma_.lower().strip() for token in doc
                   if token.lemma_ != '-PRON-'
                   and not token.is_stop
                   and token.lemma_ not in punctuations
                   and token.lemma_.isalpha()]  # LEMMATIZE & STOPWORDS
            txt = [token for token in txt if token not in custom_stop]

        elif mode == 2:
            txt = [token.text.lower().strip() for token in doc
                   if not token.is_stop
                   and token.text not in punctuations
                   and token.lemma_.isalpha()]  # STOPWORDS
            txt = [token for token in txt if token not in custom_stop]

        elif mode == 3:
            txt = [token.lemma_.lower().strip() for token in doc
                   if token.lemma_ != '-PRON-'
                   and token.lemma_ not in punctuations
                   and token.lemma_.isalpha()]  # LEMMATIZE
            txt = [token for token in txt if token not in custom_stop]

        else:
            raise Exception('Unsupported mode in preprocessing (must be 1, 2 or 3).' +
                            'The value of x was: {}'.format(mode))

        # Remove short sentences
        if len(txt) > 2:
            return ' '.join(txt)
        else:
            return None

    texts_iter = (row for row in texts)
    texts_after = [cleaning(doc, mode)
                   for doc in tqdm(nlp.pipe(texts_iter, batch_size=200), total=len(texts))]

    return texts_after
