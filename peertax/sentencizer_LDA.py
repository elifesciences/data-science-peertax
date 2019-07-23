# CUSTOM SENTENCIZER FUNCTION

# Custom sentencizer function for text preprocessing.
# The following function does the following:
#   - Remove HTML tags
#   - Remove URLs
#   - Remove question marks inside parenthesis (they mess up sentence splitting)
#   - Keep only letters, commas, colon, semicolon, period, question marks,
#     exclamation marks and hyphen
#   - Splits texts into constituent sentences: ignore et al., fig. and ex.


# INPUTS:
#   - List of documents to process (if you have a single one, declare it as a list)


# OUTPUT:
#   - For each document, a list of sentences

import html
import re
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook as tqdm
import spacy
from spacy.pipeline import Sentencizer


# Sentencizer function
def custom_sentencizer(texts):
    # disabling Named Entity Recognition for speed
    nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])
    boundary_1 = re.compile('(fig)')
    boundary_2_2 = re.compile('(et)')
    boundary_2_1 = re.compile('(al)')
    boundary_3 = re.compile('(ex)')

    # Utility functions
    def custom_seg_1(doc):
        prev = doc[0].text
        length = len(doc)
        for index, token in enumerate(doc):
            if (token.text == '.' and boundary_1.match(prev.lower()) and index != (length - 1)):
                doc[index+1].sent_start = False
            prev = token.text
        return doc

    def custom_seg_2(doc):
        length = len(doc)
        # If single token, return
        if length < 2:
            return doc
        # If multiple token, apply rule
        else:
            prev_2 = doc[0].text
            prev_1 = doc[1].text
            for index, token in enumerate(doc):
                if index > 0:
                    if (((token.text == '.') | (token.text == '.,'))
                            and boundary_2_2.match(prev_2.lower())
                            and boundary_2_1.match(prev_1.lower())
                            and index != (length - 1)):

                        if doc[index+1].text == ',':
                            doc[index+2].sent_start = False
                        else:
                            doc[index+1].sent_start = False

                    prev_1 = token.text
                    prev_2 = doc[index-1].text
            return doc

    def custom_seg_3(doc):
        prev = doc[0].text
        length = len(doc)
        for index, token in enumerate(doc):
            if (token.text == '.' and boundary_3.match(prev.lower()) and index != (length - 1)):
                doc[index+1].sent_start = False
            prev = token.text
        return doc

    def brief_cleaning_fun(text):
        text = BeautifulSoup(html.unescape(text), 'lxml').text  # remove HTML tags
        text = re.sub(r'https?://\S+', '', str(text))  # remove URLs
        # Remove question marks inside parenthesis (they mess up sentence splitting)
        text = re.sub(r'\(\?', r'\(', str(text))
        # Remove question marks inside parenthesis (they mess up sentence splitting)
        text = re.sub(r'\?\)', r'\)', str(text))
        # Remove \xa0 tags (they mess up sentence splitting)
        text = re.sub(r'[\xa0]', '', str(text))
        # Replace multiple occurrences of whitespace characters with single one
        text = re.sub(r'(\s)\1{1,}', r'\1', str(text))
        return text

    def sentence_cleaning_fun(text):
        # keep only letters, commas, colon, semicolon,
        # period, question marks, exclamation marks and hyphen
        text = re.sub(r"[^a-zA-Z0-9,'\":;.?!\(\)\-]", ' ', str(text))
        if not text:
            text = 'nan'
        return text

    def sentencization(doc):
        # Accept only documents with more than two words (one word and one punctuation.)
        if len(doc) > 2:
            text = [sentence_cleaning_fun(token.text).strip().split() for token in doc.sents]
            # Remove short sentences
            text = [' '.join(x) for x in text if len(x) > 1]
            if text:
                return text
            else:
                return 'nan'
        else:
            return 'nan'

    sentencizer = Sentencizer(punct_chars=[".", "?", "!",
                                           "\n", "\n ",
                                           "\n\n", "\n \n ",
                                           "\n\n\n", "\n \n \n ",
                                           "\n\n\n\n", "\n \n \n \n ",
                                           "\n\n\n\n\n", "\n \n \n \n \n "])
    nlp.add_pipe(sentencizer)
    nlp.add_pipe(custom_seg_1, after='sentencizer')
    nlp.add_pipe(custom_seg_2, after='custom_seg_1')
    nlp.add_pipe(custom_seg_3, after='custom_seg_2')

    brief_cleaning = (brief_cleaning_fun(row) for row in texts)
    texts_processed = [sentencization(doc) for doc in tqdm(nlp.pipe(brief_cleaning, batch_size=25),
                                                           total=len(texts))]

    return texts_processed
