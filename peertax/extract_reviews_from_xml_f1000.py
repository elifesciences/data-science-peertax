# Configuration
import os
import re
import pandas as pd
from lxml import etree
from tqdm import tqdm_notebook as tqdm
from peertax import xml

paper_folder = '../data/articles/f1000_articles/'

# Extract reviews
paper_ID = []
review_ID = []
review = []
for doc in tqdm(os.listdir(paper_folder)):
    if not doc.endswith('.xml'):
        continue
    fullname = os.path.join(paper_folder, doc)
    if os.stat(fullname).st_size != 0:
        tree = etree.parse(fullname)
        # Select article DOI
        ID = tree.findall("//article-meta/article-id[@pub-id-type='doi']")
        # Select reviews
        rev_ID = tree.findall("//sub-article/front-stub/article-id[@pub-id-type='doi']")
        rev_text = tree.findall("//sub-article[@article-type='ref-report']/body")
        for i, _ in enumerate(rev_text):
            paper_ID.append(re.sub(r'\t+', '', xml.get_text_content(ID[0])))
            review_ID.append(re.sub(r'\t+', '', xml.get_text_content(rev_ID[i])))
            review.append(re.sub(r'\t+', '', xml.get_text_content(rev_text[i])))

# Put reviews in a dataframe
df = pd.DataFrame({'manuscript_ID': paper_ID,
                   'review_ID': review_ID,
                   'review': review})

# Save the dataframe
df.to_csv('../data/reviews/f1000_reviews.csv')
